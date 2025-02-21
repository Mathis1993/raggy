import logging

from celery import shared_task
from django.db import IntegrityError

from knowledge_base.ingestion.service import DocumentIngestionService
from knowledge_base.models import Document


logger = logging.getLogger(__name__)


@shared_task
def task_handle_document_ingestion(document_id: int) -> bool:
    document = Document.objects.get(id=document_id)
    try:
        service = DocumentIngestionService(document)
        service.ingest_document()
    except IntegrityError as e:
        logger.error(f"Could not ingest document: {e}")
        document.mark_as_failed()
    except Exception as e:
        logger.error(f"Could not ingest document: {e}")
        document.mark_as_failed()
    return True

