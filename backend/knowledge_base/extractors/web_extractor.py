from llama_index.core import Document
from llama_index.readers.web import SimpleWebPageReader
from .base import DocumentExtractor


class WebExtractor(DocumentExtractor):
    def extract(self, source: str) -> Document:
        documents = SimpleWebPageReader().load_data([source])

        if not documents:
            raise ValueError(f"Content extraction from URL {source} failed.")

        return documents[0]
