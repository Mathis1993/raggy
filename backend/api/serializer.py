from rest_framework import serializers

from questions.models import Question
from knowledge_base.models import Document


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "title", "identifier", "created_at"]
