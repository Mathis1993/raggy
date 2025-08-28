from pathlib import Path

from llama_index.core import Document
from llama_index.readers.file import PDFReader

from .base import DocumentExtractor


class PDFExtractor(DocumentExtractor):
    def extract(self, source: str) -> Document:
        reader = PDFReader(return_full_document=True)
        documents = reader.load_data(file=Path(source))

        if not documents:
            raise ValueError(f"Content extraction from PDF {source} failed.")
        return documents[0]
