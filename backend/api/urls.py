from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import QuestionModelViewSet, DocumentModelViewSet

router = DefaultRouter()
router.register(r"questions", QuestionModelViewSet, basename="question")
router.register(r"documents", DocumentModelViewSet, basename="document")

app_name = "api"
urlpatterns = [
    path("", include(router.urls)),
]
