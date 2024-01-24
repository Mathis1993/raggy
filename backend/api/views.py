from django.conf import settings
from django.http import JsonResponse

from openai import OpenAI
from rest_framework.views import APIView


class QuestionAnswerView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    def post(self, request):
        question_by_user = request.data.get("question")

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

        print("GPT answered: " + str(chat_completion.choices[0].message.content))

        return JsonResponse({"answer": str(chat_completion.choices[0].message.content)})
