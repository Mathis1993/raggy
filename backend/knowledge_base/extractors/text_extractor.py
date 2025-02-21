from llama_index.core import Document, SimpleDirectoryReader
from .base import DocumentExtractor


class TextExtractor(DocumentExtractor):
    def extract(self, source: str) -> Document:
        reader = SimpleDirectoryReader(input_files=[source])
        document = reader.load_data()

        if not document:
            raise ValueError(f"Content extraction from text file {source} failed.")

        return document
