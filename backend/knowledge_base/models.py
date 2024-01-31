from django.conf import settings
from django.db import models
from langchain_community.embeddings import HuggingFaceEmbeddings
from llama_index.embeddings import LangchainEmbedding
from llama_index.extractors import TitleExtractor
from llama_index.ingestion import IngestionPipeline
from llama_index.readers import BeautifulSoupWebReader
from llama_index.text_splitter import SentenceSplitter

from core.models import TrackCreation
from knowledge_base.vector_store import initialize_milvus_store

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


class Document(TrackCreation):
    class Meta:
        db_table = "knowledge_base_documents"

    class Type(models.TextChoices):
        WEBSITE = "website"
        PDF = "pdf"
        PLAIN_TEXT = "plain_text"

    user_id = models.IntegerField()
    identifier = models.CharField(max_length=2048, unique=True)
    doc_id = models.CharField(max_length=2048, null=True)
    type = models.CharField(choices=Type.choices, max_length=255)
    title = models.CharField(max_length=1024, null=True)
    content = models.TextField(null=True)

    def ingest(self, url: str):
        if not self.pk:
            raise ValueError("Document must be saved before ingestion.")

        self._ingest(url)
        self.save()

    def _ingest(self, url: str):
        milvus_store = initialize_milvus_store(uri=f"http://{settings.MILVUS_HOST}:{settings.MILVUS_PORT}", load_collection=False)

        documents = BeautifulSoupWebReader().load_data([url])
        if len(documents) == 0:
            raise ValueError(f"Content extraction from url {url} failed.")
        document = documents[0]
        document.metadata["user_id"] = self.user_id
        document.metadata["postgres_doc_id"] = self.pk

        embedding = LangchainEmbedding(HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL))

        pipeline = IngestionPipeline(
            transformations=[
                SentenceSplitter(),
                TitleExtractor(),
                embedding,
            ],
        )
        nodes = pipeline.run(documents=[document])
        milvus_store.add([n for n in nodes if n.embedding is not None])

        self.doc_id = document.doc_id
        self.content = document.text
        if len(nodes) > 0:
            self.title = nodes[0].metadata["document_title"]
