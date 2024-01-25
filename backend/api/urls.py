from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import QuestionModelViewSet


router = DefaultRouter()
router.register(r"questions", QuestionModelViewSet, basename="question")
router.register(r"documents", QuestionModelViewSet, basename="document")

app_name = "api"
urlpatterns = [
    path("", include(router.urls)),
]
