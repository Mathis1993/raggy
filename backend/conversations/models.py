from django.db import models


class Conversation(models.Model):
    # Placeholder for now
    user_id = models.IntegerField(default=1)

    name = models.CharField(max_length=255, default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or f"Conversation {self.id}"

    def get_message_history(self):
        return self.messages.order_by("created_at")[:10]

    def add_user_message(self, text: str):
        return Message.create_user_message(conversation=self, text=text)

    def add_assistant_message(self, text: str):
        return Message.create_assistant_message(conversation=self, text=text)


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )

    text = models.TextField(default=None, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    is_user_message = models.BooleanField(default=False)
    processing_time = models.FloatField(default=0.0)

    def __str__(self):
        return self.text

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
