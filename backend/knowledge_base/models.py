import logging
from pathlib import Path

from django.conf import settings
from django.db import models
from langchain_community.embeddings import HuggingFaceEmbeddings
from llama_index import download_loader
from llama_index.embeddings import LangchainEmbedding
from llama_index.extractors import TitleExtractor, KeywordExtractor
from llama_index.ingestion import IngestionPipeline
from llama_index.readers import BeautifulSoupWebReader
from llama_index.text_splitter import SentenceSplitter

from core.models import TrackCreation
from core.utils.models import model_save
from knowledge_base.vector_store import initialize_milvus_store

logger = logging.getLogger(__name__)


class Document(TrackCreation):
    class Meta:
        db_table = "knowledge_base_documents"
        unique_together = ("user_id", "identifier")

    class Type(models.TextChoices):
        WEBSITE = "website"
        PDF = "pdf"
        PLAIN_TEXT = "plain_text"

    class Status(models.TextChoices):
        PROCESSING = "processing"
        COMPLETED = "completed"
        FAILED = "failed"

    user_id = models.IntegerField()
    identifier = models.CharField(max_length=2048)
    doc_id = models.CharField(max_length=2048, null=True)
    type = models.CharField(choices=Type.choices, max_length=255)
    title = models.CharField(max_length=1024, null=True)
    content = models.TextField(null=True)
    status = models.CharField(choices=Status.choices, max_length=255, default=Status.PROCESSING)

    url = models.URLField(null=True, blank=True, default=None)
    file = models.FileField(upload_to='documents/', null=True, blank=True, default=None)

    # Testing of metadata extraction
    keywords = models.TextField(null=True)

    def __str__(self):
        return f"{self.identifier} ({self.type})"

    @classmethod
    def create_from_url(cls, user_id: int, url: str):
        document = cls.objects.create(user_id=user_id, identifier=url, type=cls.Type.WEBSITE, url=url)
        return document

    @classmethod
    def create_from_file(cls, user_id: int, identifier: str, file: str):
        document = cls.objects.create(
            user_id=user_id,
            identifier=identifier,
            file=file,
            type=cls.Type.PDF
        )
        return document

    def ingest(self):
        if not self.pk:
            raise ValueError("Document must be saved before ingestion.")
        self._ingest()
        self.mark_as_completed(save=False)
        self.save()

    def delete_and_digest(self):
        self._digest()
        self.delete()

    @model_save(update_fields=["status"])
    def mark_as_failed(self):
        self.status = Document.Status.FAILED

    @model_save(update_fields=["status"])
    def mark_as_completed(self):
        self.status = Document.Status.COMPLETED

    def _ingest(self):
        milvus_store = initialize_milvus_store(
            uri=f"http://{settings.MILVUS_HOST}:{settings.MILVUS_PORT}",
            load_collection=False
        )

        if self.type == Document.Type.WEBSITE:
            document = self._extract_document_from_url()
        elif self.type == Document.Type.PDF:
            document = self._extract_document_from_pdf()
        else:
            raise ValueError(f"Document type {self.type} not supported.")

        document.metadata["user_id"] = self.user_id
        document.metadata["postgres_doc_id"] = self.pk

        embedding = LangchainEmbedding(HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL))

        pipeline = IngestionPipeline(
            transformations=[
                SentenceSplitter(),
                TitleExtractor(),
                KeywordExtractor(),
                embedding,
            ],
            # TODO: Can we use the vector_store parameter of the pipeline here?
        )
        nodes = pipeline.run(documents=[document])
        milvus_store.add([n for n in nodes if n.embedding is not None])
        logger.info(f"Added {len(nodes)} nodes from document.")

        self.doc_id = document.doc_id
        self.content = document.text
        self.type = Document.Type.WEBSITE
        if len(nodes) > 0:
            self.title = nodes[0].metadata["document_title"]
            keywords = ", ".join([node.metadata.get("excerpt_keywords", "") for node in nodes])
            self.keywords = keywords

    def _extract_document_from_url(self):
        url = self.url
        documents = BeautifulSoupWebReader().load_data([url])
        if len(documents) == 0:
            raise ValueError(f"Content extraction from url {url} failed.")
        document = documents[0]
        return document

    def _extract_document_from_pdf(self):
        PDFReader = download_loader("PDFReader")
        loader = PDFReader()
        documents = loader.load_data(file=Path(self.file.path))
        if len(documents) == 0:
            raise ValueError(f"Content extraction from pdf {self.file} failed.")
        return documents[0]

    def _digest(self):
        milvus_store = initialize_milvus_store(
            uri=f"http://{settings.MILVUS_HOST}:{settings.MILVUS_PORT}",
            load_collection=False
        )
        # TODO: Currently, we cannot just use the .delete() method of the milvus store as it does
        #  some weird string concatenation with the ref_doc_id. So, we implement this on our own.
        milvus_store.milvusclient.delete(collection_name=milvus_store.collection_name, pks=[self.pk])
        logger.debug(f"Successfully deleted embedding with postgres_doc_id: {self.pk}")
