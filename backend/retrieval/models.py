from django.db import models

from retrieval.tools.index import DocumentIndex


class Document(models.Model):
    name = models.CharField(max_length=255)
    doc_id = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # TODO: check if the document has already been indexed
        # TODO: add metadata to the document for better filtering/ more information
        indexer = DocumentIndex()
        indexer.insert_single_text_into_index(self.text)
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        indexer = DocumentIndex()
        indexer.index.delete_ref_doc(ref_doc_id=self.doc_id)
        super().delete(using=None, keep_parents=False)
