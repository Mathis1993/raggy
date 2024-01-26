import json
import logging

from django.http import JsonResponse
from llama_index.readers import BeautifulSoupWebReader
from rest_framework.viewsets import ViewSet

from api.serializer import QuestionSerializer, DocumentSerializer
from questions.models import Question
from retrieval.models import Document
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

        query_engine = QueryEngine()
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

        document = BeautifulSoupWebReader().load_data([requested_url])[0]
        logger.info(f"Extracted text from url: {document.text}")
        document = self.model.objects.create(
            name=requested_url,
            doc_id=document.get_doc_id(),
            url=requested_url,
            text=document.text,
        )
        logger.info(f"Created document: {document}")
        return JsonResponse({"document": DocumentSerializer(document).data})
