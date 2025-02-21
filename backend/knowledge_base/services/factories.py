from django.conf import settings
from knowledge_base.extractors import ExtractorRepository
from knowledge_base.vector_store import initialize_milvus_store
from .document_ingestion import DocumentIngestionService, NodeProcessor, DocumentMetadataHandler


def create_document_ingestion_service(document) -> DocumentIngestionService:
    """Factory function to create DocumentIngestionService with all dependencies"""
    vector_store = initialize_milvus_store(
        uri=f"http://{settings.MILVUS_HOST}:{settings.MILVUS_PORT}", load_collection=False
    )

    node_processor = NodeProcessor(
        chunk_size=settings.CHUNK_SIZE, chunk_overlap=settings.CHUNK_OVERLAP
    )

    return DocumentIngestionService(
        document=document,
        extractor_repository=ExtractorRepository(),
        vector_store=vector_store,
        node_processor=node_processor,
        metadata_updater=DocumentMetadataHandler(),
    )
