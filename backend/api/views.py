import http
import logging

from django.conf import settings
from django.db import IntegrityError
from django.http import JsonResponse
from langchain_community.embeddings import HuggingFaceEmbeddings
from llama_index import ServiceContext, StorageContext, VectorStoreIndex
from llama_index.embeddings import LangchainEmbedding
from rest_framework.viewsets import ViewSet

from api.serializer import QuestionSerializer, DocumentSerializer
from knowledge_base.models import Document, EMBEDDING_MODEL
from knowledge_base.vector_store import initialize_milvus_store
from questions.models import Question
from retrieval.tools.query_engine import QueryEngine

logger = logging.getLogger(__name__)


class QuestionModelViewSet(ViewSet):

    model = Question

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list(self, request):
        questions = Question.objects.all().order_by("-created_at")[0:5]
        return JsonResponse({"questions": QuestionSerializer(questions, many=True).data})

    def retrieve(self, request, pk=None):
        question = Question.objects.get(pk=pk)
        return JsonResponse({"question": QuestionSerializer(question).data})

    def create(self, request):
        question_by_user = request.data.get("question")

        question = Question.objects.create(question=question_by_user)

        if not question_by_user:
            return JsonResponse({"error": "No question provided"})

        # query_engine = QueryEngine()
        # answer = query_engine.query(question_by_user)
        milvus_store = initialize_milvus_store(uri=f"http://{settings.MILVUS_HOST}:{settings.MILVUS_PORT}", load_collection=True)
        embedding = LangchainEmbedding(HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL))
        service_context = ServiceContext.from_defaults(embed_model=embedding)
        storage_context = StorageContext.from_defaults(vector_store=milvus_store)
        index = VectorStoreIndex.from_vector_store(vector_store=milvus_store, storage_context=storage_context, service_context=service_context)
        query_engine = index.as_query_engine()
        answer = query_engine.query(question_by_user)
        question.answer = answer
        question.save()
        return JsonResponse({"question": QuestionSerializer(question).data})


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
            document = Document.objects.create(user_id=user_id, identifier=requested_url).ingest(requested_url)
        except IntegrityError as e:
            logger.error(f"Could not ingest document: {e}")
            return JsonResponse({"error": f"Document with url {requested_url} seems to exist already"}, status=http.HTTPStatus.BAD_REQUEST)
        except Exception as e:
            logger.error(f"Could not ingest document: {e}")
            return JsonResponse({"error": str(e)}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)
        logger.info(f"Created document: {document}")
        return JsonResponse({"document": DocumentSerializer(document).data})
