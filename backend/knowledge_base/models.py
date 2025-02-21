from __future__ import annotations

from django.conf import settings
from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile

from knowledge_base.ingestion.service import DocumentMetadataHandler
from core.models import TrackCreation
from core.utils.models import model_save


def user_directory_path(instance, filename) -> str:
    """Generate upload path for user documents"""
    return f"documents/user_{instance.user.id}/{filename}"


class Document(TrackCreation):
    """
    Represents a document in the knowledge base that can be processed and queried.
    """
    class Meta:
        db_table = "knowledge_base_documents"
        unique_together = ("user_id", "identifier")

    class Type(models.TextChoices):
        WEBSITE = "WEBSITE", "Website"
        PDF = "PDF", "PDF"
        PLAIN_TEXT = "PLAIN_TEXT", "Plain Text"
        WORD = "WORD", "Word"

    class Status(models.TextChoices):
        PROCESSING = "PROCESSING", "Processing"
        COMPLETED = "COMPLETED", "Completed"
        FAILED = "FAILED", "Failed"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="documents"
    )
    identifier = models.CharField(max_length=2048)
    doc_id = models.CharField(max_length=2048, null=True)
    type = models.CharField(choices=Type.choices, max_length=255)
    title = models.CharField(max_length=1024, null=True)
    content = models.TextField(null=True)
    status = models.CharField(choices=Status.choices, max_length=255, default=Status.PROCESSING)
    url = models.URLField(null=True, blank=True)
    file = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    keywords = models.TextField(null=True)

    def __str__(self) -> str:
        return f"{self.identifier} ({self.type})"

    @property
    def source(self) -> str:
        """Get the document source (URL or file path)"""
        return self.url if self.type == self.Type.WEBSITE else self.file.path

    @classmethod
    def create_from_url(cls, user_id: int, url: str) -> Document:
        """Create a document from a URL"""
        return cls.objects.create(user_id=user_id, identifier=url, type=cls.Type.WEBSITE, url=url)

    @classmethod
    def create_from_file(
        cls, user_id: int, file: str, document_name: str, file_type: Type
    ) -> Document:
        """Create a document from a file"""
        return cls.objects.create(
            user_id=user_id, file=file, type=file_type, identifier=document_name
        )

    @model_save(update_fields=["status"])
    def mark_as_failed(self) -> None:
        """Mark document processing as failed"""
        self.status = self.Status.FAILED

    @model_save(update_fields=["status"])
    def mark_as_completed(self) -> None:
        """Mark document processing as completed"""
        self.status = self.Status.COMPLETED

    @staticmethod
    def infer_file_type(file: InMemoryUploadedFile) -> "Document.Type":
        """Infer document type from file extension"""
        if file.name.endswith(".pdf"):
            return Document.Type.PDF
        if file.name.endswith(".doc") or file.name.endswith(".docx"):
            return Document.Type.WORD
        return Document.Type.PLAIN_TEXT

    def delete_and_digest(self) -> None:
        """Delete document and clean up related data"""
        from knowledge_base.ingestion.service import DocumentIngestionService
        from knowledge_base.extractors import ExtractorRepository

        service = DocumentIngestionService(
            document=self,
            extractor_repository=ExtractorRepository(),
            metadata_updater=DocumentMetadataHandler(),
        )
        service.digest_document()
        super().delete()
