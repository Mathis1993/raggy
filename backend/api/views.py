from django.conf import settings
from django.http import JsonResponse
from openai import OpenAI
from rest_framework.viewsets import ViewSet

from api.serializer import QuestionSerializer
from questions.models import Question


class QuestionModelViewSet(ViewSet):

    model = Question

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    def list(self, request):
        questions = Question.objects.all()
        return JsonResponse({"questions": QuestionSerializer(questions, many=True).data})

    def create(self, request):
        question_by_user = request.data.get("question")

        question = Question.objects.create(
            question=question_by_user,
            answer="",
        )

        if not question_by_user:
            print("No question provided")
            return JsonResponse({"error": "No question provided"})

        print("Asking GPT: " +question_by_user)

        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Answer shortly: " + question_by_user,
                }
            ],
            model="gpt-3.5-turbo",
        )
        answer = str(chat_completion.choices[0].message.content)
        question.answer = answer
        question.save()

        print("GPT answered: " + answer)

        return JsonResponse({"answer": answer})
