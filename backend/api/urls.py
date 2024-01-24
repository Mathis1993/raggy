from django.urls import path

from backend.api.views import QuestionAnswerView

app_name = "api"
urlpatterns = [
    path("questions/create", QuestionAnswerView.as_view(), name="create-question")
]
