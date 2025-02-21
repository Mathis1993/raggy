from typing import Dict, Type
from django.conf import settings
from .base import DocumentExtractor
from .pdf_extractor import PDFExtractor
from .web_extractor import WebExtractor
from .word_extractor import WordExtractor
from .text_extractor import TextExtractor


class ExtractorRepository:
    """Repository for managing document extractors"""

    def __init__(self):
        self._extractors: Dict[str, Type[DocumentExtractor]] = {}
        self._register_default_extractors()

    def _register_default_extractors(self):
        """Register the default set of extractors"""
        from knowledge_base.models import Document

        # Use an explicit mapping between Document types and extractors
        self._type_mapping = {
            Document.Type.PDF: PDFExtractor,
            Document.Type.WEBSITE: WebExtractor,
            Document.Type.WORD: WordExtractor,
            Document.Type.PLAIN_TEXT: TextExtractor,
        }

        # Register all default extractors
        for doc_type, extractor_class in self._type_mapping.items():
            self.register(doc_type, extractor_class)

    def register(self, key: str, extractor_class: Type[DocumentExtractor]) -> None:
        """Register a new extractor class for a given key

        Args:
            key: The document type key
            extractor_class: The extractor class to register

        Raises:
            ValueError: If extractor_class doesn't implement DocumentExtractor
        """
        if not issubclass(extractor_class, DocumentExtractor):
            raise ValueError(
                f"Extractor class {extractor_class.__name__} must implement DocumentExtractor interface"
            )

        self._extractors[key] = extractor_class

    def get_extractor(self, key: str) -> DocumentExtractor:
        """Get an instance of the appropriate extractor

        Args:
            key: The key identifying the type of extractor needed

        Returns:
            DocumentExtractor: An instance of the appropriate extractor

        Raises:
            ValueError: If no extractor is registered for the given key
        """
        extractor_class = self._extractors.get(key)
        if not extractor_class:
            supported_types = ", ".join(self._extractors.keys())
            raise ValueError(
                f"No extractor registered for type: {key}. Supported types are: {supported_types}"
            )

        return extractor_class()
