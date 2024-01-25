from django.db import models

from retrieval.tools.index import DocumentIndex


class Document(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        indexer = DocumentIndex()
        indexer.embed_text(self.text)