import logging

import llama_index
from django.conf import settings
from langchain_community.embeddings import HuggingFaceEmbeddings
from llama_index.data_structs import Node
from llama_index.embeddings import LangchainEmbedding
from llama_index.extractors import TitleExtractor, KeywordExtractor
from llama_index.ingestion import IngestionPipeline
from llama_index.node_parser import SentenceSplitter

from knowledge_base.models import Document
from knowledge_base.utils.document_extractor import DocumentExtractor
from knowledge_base.vector_store import initialize_milvus_store

logger = logging.getLogger(__name__)


class DocumentIngestionService:

    def __init__(self, document: Document):
        self.document = document
        self.milvus_store = initialize_milvus_store(
                uri=f"http://{settings.MILVUS_HOST}:{settings.MILVUS_PORT}",
                load_collection=False
            )

    def ingest_document(self):
        """ Orchestrates the ingestion of a document, whether it's from a URL or a file."""
        try:
            if self.document.type == Document.Type.WEBSITE:
                llama_document: llama_index.Document = DocumentExtractor.extract_content_from_url(
                    self.document.url
                )
            elif self.document.type == Document.Type.PDF:
                llama_document: llama_index.Document = DocumentExtractor.extract_content_from_pdf(
                    self.document.file.path
                )
            else:
                raise ValueError(f"Unsupported document type: {self.document.type}")

            nodes: [Node] = self._extract_nodes(llama_document)
            self._store_nodes(nodes)
            self._update_document(llama_document, nodes)
            self.document.mark_as_completed()
        except Exception as e:
            logger.error(f"Failed to ingest document {self.document.id}: {e}")
            self.document.mark_as_failed()

    def _extract_nodes(self, llama_document: llama_index.Document):
        llama_document.metadata["user_id"] = self.document.user_id
        llama_document.metadata["postgres_doc_id"] = self.document.id

        embedding = LangchainEmbedding(HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL))
        pipeline = IngestionPipeline(
            transformations=[
                SentenceSplitter(),
                TitleExtractor(),
                KeywordExtractor(),
                embedding,
            ],
        )
        nodes = pipeline.run(documents=[llama_document])
        return nodes

    def _store_nodes(self, nodes: [Node]):
        self.milvus_store.add([n for n in nodes if n.embedding is not None])
        logger.info(f"Added {len(nodes)} nodes from document.")

    def _update_document(self, llama_document: llama_index.Document, nodes: [Node]):
        self.document.doc_id = llama_document.doc_id
        self.document.content = llama_document.text
        if len(nodes) > 0:
            self.document.title = nodes[0].metadata["document_title"]
            keywords = ", ".join([node.metadata.get("excerpt_keywords", "") for node in nodes])
            self.document.keywords = keywords
        self.document.save()

    def digest_document(self):
        # TODO: Currently, we cannot just use the .delete() method of the milvus store as it does
        #  some weird string concatenation with the ref_doc_id. So, we implement this on our own.
        self.milvus_store.milvusclient.delete(
            collection_name=self.milvus_store.collection_name, pks=[self.document.pk]
        )
        logger.debug(f"Successfully deleted embedding with postgres_doc_id: {self.document.pk}")
