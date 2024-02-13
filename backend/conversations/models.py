from typing import List

from django.conf import settings
from django.db import models
from llama_index.tools import ToolOutput

from core.models import TrackCreationAndUpdates
from core.utils.models import model_save
from knowledge_base.models import Document


class Conversation(TrackCreationAndUpdates):

    class Status(models.TextChoices):
        RUNNING = "RUNNING", "Running"
        COMPLETED = "COMPLETED", "Completed"
        FAILED = "FAILED", "Failed"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="conversations")
    name = models.CharField(max_length=255, default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.COMPLETED)

    def __str__(self):
        return self.name or f"Conversation {self.id}"

    @model_save(update_fields=["status"])
    def mark_as_running(self):
        self.status = self.Status.RUNNING

    @model_save(update_fields=["status"])
    def mark_as_completed(self):
        self.status = self.Status.COMPLETED

    @model_save(update_fields=["status"])
    def mark_as_failed(self):
        self.status = self.Status.FAILED

    def get_message_history(self):
        return self.messages.order_by("created_at")[:10]

    def add_user_message(self, text: str):
        return Message.create_user_message(conversation=self, text=text)

    def add_assistant_message(self, text: str):
        return Message.create_assistant_message(conversation=self, text=text)


class Message(TrackCreationAndUpdates):
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )

    text = models.TextField(default=None, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    is_user_message = models.BooleanField(default=False)
    processing_time = models.FloatField(default=0.0)

    source_documents = models.ManyToManyField("knowledge_base.Document", related_name="messages")

    def __str__(self):
        return self.text

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.conversation.name:
            # TODO: generate name using LLM
            self.conversation.name = self.text[:25]
            self.conversation.save()
        super().save(force_insert, force_update, using, update_fields)

    @classmethod
    def create_user_message(cls, conversation: Conversation, text: str) -> "Message":
        return cls.objects.create(
            conversation=conversation,
            text=text,
            is_user_message=True,
        )

    @classmethod
    def create_assistant_message(cls, conversation: Conversation, text: str) -> "Message":
        return cls.objects.create(
            conversation=conversation,
            text=text,
            is_user_message=False,
        )

    def add_sources(self, source_nodes: List[ToolOutput]):
        source_document_ids = [source.metadata.get("postgres_doc_id", None) for source in source_nodes]
        source_documents = Document.objects.filter(id__in=set(list(source_document_ids)))
        self.source_documents.add(*source_documents)

