from rest_framework import serializers

from conversations.models import Conversation, Message, MessageSourceDocument
from knowledge_base.models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "title", "identifier", "created_at", "status", "type"]


class DocumentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "title", "identifier", "created_at", "status", "type", "keywords"]


class MessageSourceDocumentSerializer(serializers.ModelSerializer):
    document = DocumentSerializer(read_only=True)
    excerpt = serializers.CharField(read_only=True)

    class Meta:
        model = MessageSourceDocument
        fields = ["document", "excerpt"]


class MessageSerializer(serializers.ModelSerializer):
    is_user_message = serializers.BooleanField(read_only=True)
    text = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M")

    sources = MessageSourceDocumentSerializer(many=True, read_only=True, source="messagesourcedocument_set")

    class Meta:
        model = Message
        fields = ["is_user_message", "text", "created_at", "sources"]


class ConversationDetailSerializer(serializers.Serializer):
    messages = MessageSerializer(many=True, read_only=True)
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Conversation
        fields = ["id", "name", "created_at", "messages"]


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ["id", "name", "created_at", "user"]