from __future__ import annotations

from typing import Union

from django.conf import settings
from django.db import models

from core.models import TrackCreation
from core.utils.models import model_save
from knowledge_base.utils.document_ingestion import DocumentIngestionService


def user_directory_path(instance, filename):
    return "documents/user_{0}/{1}".format(instance.user.id, filename)


class Document(TrackCreation):
    class Meta:
        db_table = "knowledge_base_documents"
        unique_together = ("user_id", "identifier")

    class Type(models.TextChoices):
        WEBSITE = "website", "Website"
        PDF = "pdf", "PDF"
        PLAIN_TEXT = "plain_text", "Plain Text"
        WORD = "word", "Word"

    class Status(models.TextChoices):
        PROCESSING = "processing", "Processing"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="documents")
    identifier = models.CharField(max_length=2048)
    doc_id = models.CharField(max_length=2048, null=True)
    type = models.CharField(choices=Type.choices, max_length=255)
    title = models.CharField(max_length=1024, null=True)
    content = models.TextField(null=True)
    status = models.CharField(choices=Status.choices, max_length=255, default=Status.PROCESSING)
    url = models.URLField(null=True, blank=True)
    file = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    keywords = models.TextField(null=True)

    def __str__(self):
        return f"{self.identifier} ({self.type})"

    @classmethod
    def create_from_url(cls, user_id: int, url: str):
        return cls.objects.create(user_id=user_id, identifier=url, type=cls.Type.WEBSITE, url=url)

    @classmethod
    def create_from_file(cls, user_id: int, file: str, document_name: str, file_type: Document.Type) -> Document:
        return cls.objects.create(user_id=user_id, file=file, type=file_type, identifier=document_name)

    def ingest(self):
        if not self.pk:
            raise ValueError("Document must be saved before ingestion.")
        DocumentIngestionService(self).ingest_document()

    def delete_and_digest(self):
        DocumentIngestionService(self).digest_document()
        self.delete()

    @model_save(update_fields=["status"])
    def mark_as_failed(self):
        self.status = self.Status.FAILED

    @model_save(update_fields=["status"])
    def mark_as_completed(self):
        self.status = self.Status.COMPLETED
