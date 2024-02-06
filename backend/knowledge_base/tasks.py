import logging

from celery import shared_task
from django.db import IntegrityError

from knowledge_base.models import Document


logger = logging.getLogger(__name__)


@shared_task
def task_handle_document_ingestion(document_id: int, url: str) -> None:
    try:
        document = Document.objects.get(id=document_id)
        document.ingest(url)
    except IntegrityError as e:
        logger.error(f"Could not ingest document: {e}")
    except Exception as e:
        logger.error(f"Could not ingest document: {e}")
    return True

