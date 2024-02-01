from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import DocumentModelViewSet, ConversationModelViewSet, MessageModelViewSet

router = DefaultRouter()
router.register(r"conversations", ConversationModelViewSet, basename="conversation")
router.register(r"conversations/(?P<conversation_id>\d+)/messages", MessageModelViewSet, basename="message")
router.register(r"documents", DocumentModelViewSet, basename="document")

app_name = "api"
urlpatterns = [
    path("", include(router.urls)),
]
