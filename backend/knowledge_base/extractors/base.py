from abc import ABC, abstractmethod
from llama_index.core import Document


class DocumentExtractor(ABC):
    """Base interface for document extractors"""

    @abstractmethod
    def extract(self, source: str) -> Document:
        """Extract content from the given source

        Args:
            source: Path to file or URL to extract from

        Returns:
            Document: Extracted llama_index Document

        Raises:
            ValueError: If extraction fails
        """
        pass
