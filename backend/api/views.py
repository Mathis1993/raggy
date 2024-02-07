import json
import json
import logging

from django.http import JsonResponse
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.serializer import ConversationSerializer, ConversationDetailSerializer, \
    MessageSerializer
from api.serializer import DocumentSerializer
from conversations.models import Conversation
from conversations.tasks import task_handle_user_message
from knowledge_base.models import Document
from knowledge_base.tasks import task_handle_document_ingestion

logger = logging.getLogger(__name__)


class ConversationModelViewSet(ModelViewSet):
    model = Conversation
    # TODO: add permissions, e.g. IsAuthenticated
    permission_classes = []

    def get_queryset(self):
        # TODO: filter by user
        return self.model.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ConversationDetailSerializer
        return ConversationSerializer


class MessageModelViewSet(ModelViewSet):
    model = Conversation
    permission_classes = []
    serializer_class = MessageSerializer

    def get_queryset(self):
        conversation_id = self.kwargs["conversation_id"]
        # TODO: filter by user
        conversation = get_object_or_404(Conversation, id=conversation_id)
        return conversation.messages.all()

    def create(self, request, *args, **kwargs):
        data = json.loads(request.body.decode("utf-8"))
        conversation_id, message = data["conversation_id"], data["message"]
        conversation = get_object_or_404(Conversation, id=int(conversation_id))
        task_handle_user_message(conversation.id, message)
        return Response(ConversationDetailSerializer(conversation).data)


class DocumentModelViewSet(ModelViewSet):
    model = Document

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_queryset(self):
        # TODO: filter by user
        return self.model.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            # TODO: Add a serializer for the detail view
            return DocumentSerializer
        return DocumentSerializer

    def create(self, request, *args, **kwargs):
        requested_url = request.data.get("document_url")

        # make sure the url is valid
        if "http" not in requested_url:
            requested_url = "https://" + requested_url

        # ToDo(ME-31.01.24): Extract user_id from request
        user_id = 1
        document = Document.objects.create(
            user_id=user_id, identifier=requested_url, status=Document.Status.PROCESSING
        )
        task = task_handle_document_ingestion.apply_async(
            kwargs={"document_id": document.id, "url": requested_url}
        )

        # Log the task details
        logger.info(task)

        return JsonResponse({"document": DocumentSerializer(document).data})

    def destroy(self, request, *args, **kwargs):
        document = self.get_object()
        document.delete_and_digest()
        return JsonResponse({"document": DocumentSerializer(document).data})