import logging
from typing import List

from django.conf import settings
from llama_index.core import Document
from llama_index.core.data_structs import Node
from llama_index.core.extractors import TitleExtractor, KeywordExtractor
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding

from knowledge_base.extractors import ExtractorRepository
from knowledge_base.vector_store import VectorStore

logger = logging.getLogger(__name__)


class NodeProcessor:
    """Handles the processing of documents into nodes with embeddings"""

    def __init__(self, chunk_size: int, chunk_overlap: int):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def process_document(self, document: Document, metadata: dict) -> List[Node]:
        """Process a document into nodes with embeddings"""
        document.metadata.update(metadata)

        pipeline = IngestionPipeline(
            transformations=[
                SentenceSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap),
                TitleExtractor(),
                KeywordExtractor(),
                OpenAIEmbedding(),
            ],
        )
        return pipeline.run(documents=[document])


class DocumentMetadataHandler:
    """Handles document metadata based on extracted nodes"""

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
        extractor_repository: ExtractorRepository,
        vector_store: VectorStore,
        node_processor: NodeProcessor,
        metadata_updater: DocumentMetadataHandler,
    ):
        self.document = document
        self.extractor_repository = extractor_repository
        self.vector_store = vector_store
        self.node_processor = node_processor
        self.metadata_updater = metadata_updater

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
        return self.node_processor.process_document(llama_document, metadata)

    def _store_nodes(self, nodes: List[Node]) -> None:
        """Store nodes in vector store"""
        nodes_to_store = [n for n in nodes if n.embedding is not None]
        logger.info(f"Storing {len(nodes_to_store)} nodes with embeddings.")
        self.vector_store.add(nodes_to_store)

    def digest_document(self) -> None:
        """Remove document nodes from vector store"""
        self.vector_store.delete(self.document.pk)
        logger.debug(f"Successfully deleted embedding with postgres_doc_id: {self.document.pk}")
