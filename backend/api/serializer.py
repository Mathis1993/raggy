from rest_framework import serializers

from conversations.models import Conversation, Message
from questions.models import Question
from retrieval.models import Document


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "name", "url", "created_at"]


class MessageSerializer(serializers.Serializer):
    class Meta:
        model = Message
        fields = "__all__"


class ConversationSerializer(serializers.Serializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = "__all__"
