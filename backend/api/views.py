import requests
from django.conf import settings
from django.http import JsonResponse
from openai import OpenAI
from rest_framework.viewsets import ViewSet

from api.serializer import QuestionSerializer, DocumentSerializer
from questions.models import Question
from retrieval.models import Document
from retrieval.tools.query_engine import QueryEngine


class QuestionModelViewSet(ViewSet):

    model = Question

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list(self, request):
        questions = Question.objects.all()
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
        return JsonResponse({"answer": answer})


class DocumentModelViewSet(ViewSet):
    model = Question

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    def list(self, request):
        documents = Document.objects.all()
        return JsonResponse({"documents": DocumentSerializer(documents, many=True).data})

    def retrieve(self, request, pk=None):
        document = Document.objects.get(pk=pk)
        return JsonResponse({"document": DocumentSerializer(document).data})

    def create(self, request):
        requested_url = request.data.get("url")
        html_text = requests.get(requested_url).text
        document = Document.objects.create(
            name=requested_url,
            url=requested_url,
            text=html_text,
        )
        return JsonResponse({"document": DocumentSerializer(document).data})
