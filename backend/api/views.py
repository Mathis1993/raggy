import http
import logging

from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ViewSet, ModelViewSet

from api.serializer import ConversationSerializer, ConversationDetailSerializer, \
    MessageSerializer
from api.serializer import DocumentSerializer
from conversations.models import Conversation
from conversations.tasks import task_handle_user_message
from knowledge_base.models import Document

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
        conversation_id, message = self.kwargs["conversation_id"], self.kwargs["message"]
        conversation = get_object_or_404(Conversation, id=conversation_id)
        text = request.data.get("text")
        task_handle_user_message(conversation, text)
        return JsonResponse({"message": "Message received"})


class DocumentModelViewSet(ViewSet):
    model = Document

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list(self, request):
        documents = self.model.objects.all()
        return JsonResponse({"documents": DocumentSerializer(documents, many=True).data})

    def retrieve(self, request, pk=None):
        document = self.model.objects.get(pk=pk)
        return JsonResponse({"document": DocumentSerializer(document).data})

    def delete(self, request, pk=None):
        document = self.model.objects.get(pk=pk)
        document.delete()
        return JsonResponse({"document": DocumentSerializer(document).data})

    def create(self, request):
        requested_url = request.data.get("document_url")

        # make sure the url is valid
        if not "http" in requested_url:
            requested_url = "https://" + requested_url

        # ToDo(ME-31.01.24): Extract user_id from request
        user_id = 1
        try:
            document = Document.objects.create(user_id=user_id, identifier=requested_url)
            document.ingest(url=requested_url)
        except IntegrityError as e:
            logger.error(f"Could not ingest document: {e}")
            return JsonResponse({"error": f"Document with url {requested_url} seems to exist already"}, status=http.HTTPStatus.BAD_REQUEST)
        except Exception as e:
            logger.error(f"Could not ingest document: {e}")
            return JsonResponse({"error": str(e)}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)
        logger.info(f"Created document: {document}")
        return JsonResponse({"document": DocumentSerializer(document).data})
