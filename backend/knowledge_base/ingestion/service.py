import logging
from typing import List

from django.conf import settings
from llama_index.core import Document
from llama_index.core.data_structs import Node
from llama_index.core.extractors import TitleExtractor
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding

from knowledge_base.extractors import ExtractorRepository
from knowledge_base.vector_store import vector_store

logger = logging.getLogger(__name__)


class DocumentMetadataHandler:
    """Handles updating document metadata based on extracted nodes"""

    @staticmethod
    def update(document, llama_document: Document, nodes: List[Node]) -> None:
        document.doc_id = llama_document.doc_id
        document.content = llama_document.text

        if nodes:
            document.title = nodes[0].metadata["document_title"]
            keywords = ", ".join(node.metadata.get("excerpt_keywords", "") for node in nodes)
            document.keywords = keywords

        document.save()


class DocumentIngestionService:
    """Orchestrates the document ingestion process"""

    def __init__(
        self,
        document,
        extractor_repository: ExtractorRepository = None,
        metadata_updater: DocumentMetadataHandler = None,
        chunk_size: int = settings.CHUNK_SIZE,
        chunk_overlap: int = settings.CHUNK_OVERLAP,
    ):
        self.document = document
        self.vector_store = vector_store
        self.extractor_repository = extractor_repository or ExtractorRepository()
        self.metadata_updater = metadata_updater or DocumentMetadataHandler()
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def ingest_document(self) -> None:
        """Orchestrates the ingestion of a document"""
        try:
            llama_document = self._extract_content()
            nodes = self._process_nodes(llama_document)
            self._store_nodes(nodes)
            self.metadata_updater.update(self.document, llama_document, nodes)
            self.document.mark_as_completed()

        except Exception as e:
            logger.error(f"Failed to ingest document {self.document.id}: {e}")
            self.document.mark_as_failed()
            raise

    def _extract_content(self) -> Document:
        """Extract content from the document using appropriate extractor"""
        extractor = self.extractor_repository.get_extractor(self.document.type)
        source = self.document.url if self.document.type == "WEBSITE" else self.document.file.path
        return extractor.extract(source)

    def _process_nodes(self, llama_document: Document) -> List[Node]:
        """Process document into nodes with embeddings"""
        metadata = {"user_id": self.document.user_id, "postgres_doc_id": self.document.id}
        llama_document.metadata.update(metadata)

        pipeline = IngestionPipeline(
            transformations=[
                SentenceSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap),
                TitleExtractor(),
                # KeywordExtractor(),
                OpenAIEmbedding(),
            ],
            # Remove vector_store from pipeline to handle storage separately
        )
        nodes = pipeline.run(documents=[llama_document])
        logger.info(f"Created {len(nodes)} nodes from document {self.document.id}")
        return nodes

    def _store_nodes(self, nodes: List[Node]) -> None:
        """Store nodes in vector store"""
        nodes_to_store = [n for n in nodes if n.embedding is not None]
        logger.info(
            f"Storing {len(nodes_to_store)} nodes with embeddings for document {self.document.id}"
        )
        if not nodes_to_store:
            logger.warning(f"No nodes with embeddings found for document {self.document.id}")
            return
        self.vector_store.store.add(nodes_to_store)

    def digest_document(self) -> None:
        """Remove document nodes from vector store"""
        try:
            self.vector_store.store.delete(self.document.pk)
            logger.debug(f"Successfully deleted embedding with postgres_doc_id: {self.document.pk}")
        except Exception as e:
            logger.error(
                f"Failed to delete embedding with postgres_doc_id: {self.document.pk}: {e}"
            )
