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
    content = serializers.SerializerMethodField()
    highlighted_content = serializers.SerializerMethodField()

    CONTEXT_CHARS = 100  # Number of characters to include before and after the excerpt

    def get_content(self, obj):
        """Get the full content with context"""
        doc_content = obj.document.content
        if not doc_content:
            return ""

        start = max(0, obj.start_char_idx - self.CONTEXT_CHARS)
        end = min(len(doc_content), obj.end_char_idx + self.CONTEXT_CHARS)

        return doc_content[start:end]

    def get_highlighted_content(self, obj):
        """Get information about which part should be highlighted"""
        if not obj.document.content:
            return {"start": 0, "end": 0}

        # Adjust highlight positions relative to the context window
        context_start = max(0, obj.start_char_idx - self.CONTEXT_CHARS)
        highlight_start = obj.start_char_idx - context_start
        highlight_end = obj.end_char_idx - context_start

        return {"start": highlight_start, "end": highlight_end}

    class Meta:
        model = MessageSourceDocument
        fields = ["document", "content", "highlighted_content"]


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