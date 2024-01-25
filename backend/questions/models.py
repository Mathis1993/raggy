from django.db import models


class Question(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField(null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question
