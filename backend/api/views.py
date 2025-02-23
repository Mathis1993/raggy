import logging
import os

from django.http import JsonResponse, Http404, FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.serializer import ConversationSerializer, ConversationDetailSerializer, \
    MessageSerializer, DocumentDetailSerializer
from api.serializer import DocumentSerializer
from conversations.models import Conversation
from conversations.tasks import task_handle_user_message
from core.utils.utils import UrlStr
from knowledge_base.models import Document
from knowledge_base.tasks import task_handle_document_ingestion

logger = logging.getLogger(__name__)


class ConversationModelViewSet(ModelViewSet):
    model = Conversation

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by("-created_at")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ConversationDetailSerializer
        return ConversationSerializer

    def create(self, request, *args, **kwargs):
        request.data["user"] = self.request.user.id
        return super().create(request, *args, **kwargs)


class MessageModelViewSet(ModelViewSet):
    model = Conversation
    serializer_class = MessageSerializer

    def get_queryset(self):
        conversation_id = self.kwargs["conversation_id"]
        conversation = get_object_or_404(Conversation, id=conversation_id, user=self.request.user)
        return conversation.messages.all().order_by("-created_at")

    def create(self, request, *args, **kwargs):
        data = request.data
        conversation_id, message = data["conversation_id"], data["message"]
        conversation = get_object_or_404(Conversation, id=int(conversation_id), user=self.request.user)
        conversation.mark_as_running()
        conversation.add_user_message(message)
        task_handle_user_message.delay(conversation.id, message)
        return Response(ConversationDetailSerializer(conversation).data)


class DocumentModelViewSet(ModelViewSet):
    model = Document
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["type"]
    search_fields = ["title", "identifier"]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by("-created_at")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return DocumentDetailSerializer
        return DocumentSerializer

    @action(detail=False, methods=['post'], url_path='create_from_url')
    def create_from_url(self, request, *args, **kwargs):
        requested_url = request.data.get("document_url")
        try:
            requested_url = UrlStr(requested_url)
        except Exception as e:
            logger.info(f"Failed to validate URL: {str(e)}")
            return JsonResponse({"error": f"Invalid URL: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        user_id = self.request.user.id
        document = Document.create_from_url(user_id, requested_url)
        task_handle_document_ingestion.delay(document_id=document.id)
        return JsonResponse({"document": DocumentSerializer(document).data})

    @action(detail=False, methods=['post'], url_path='upload')
    def upload_file(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        document_name = request.POST.get('document_name')
        if not file:
            return JsonResponse({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        user_id = self.request.user.id
        file_type = Document.infer_file_type(file)

        if document_name:
            file_extension = file.name.split(".")[-1]
            doc_name = document_name.replace(" ", "_")
            file.name = f"{doc_name}.{file_extension}"

        document = Document.create_from_file(
            user_id=user_id, file=file, document_name=document_name, file_type=file_type
        )
        task_handle_document_ingestion.delay(document_id=document.id)
        return JsonResponse({"document": DocumentSerializer(document).data}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        document = self.get_object()
        document.delete_and_digest()
        return JsonResponse({"document": DocumentSerializer(document).data})

    @action(detail=False, methods=["get"], url_path="download/(?P<pk>[0-9]+)")
    def file_download(self, request, *args, **kwargs):
        document = self.get_object()
        if not document.user == self.request.user:
            raise Http404("Document not found.")

        if not document.file:
            raise Http404("Document does not have an attached file.")

        file_path = document.file.path
        if not os.path.exists(file_path):
            raise Http404("The requested file was not found on the server.")

        response = FileResponse(open(file_path, 'rb'), content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(file_path)
        return response
