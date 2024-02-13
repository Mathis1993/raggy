from rest_framework import serializers

from conversations.models import Conversation, Message
from knowledge_base.models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "title", "identifier", "created_at", "status", "type"]


class DocumentDetailSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ["id", "title", "identifier", "created_at", "status", "type", "keywords", "file_url"]

    def get_file_url(self, document):
        request = self.context.get("request")
        if document.file:
            file_url = document.file.url
            return request.build_absolute_uri(file_url)
        return None


class MessageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    is_user_message = serializers.BooleanField(read_only=True)
    text = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M")

    sources = DocumentSerializer(many=True, read_only=True, source="source_documents")

    class Meta:
        model = Message
        fields = "__all__"


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