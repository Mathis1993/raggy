from llama_index.core import Document, SimpleDirectoryReader
from .base import DocumentExtractor


class TextExtractor(DocumentExtractor):
    def extract(self, source: str) -> Document:
        reader = SimpleDirectoryReader(input_files=[source])
        documents = reader.load_data()

        if not documents:
            raise ValueError(f"Content extraction from text file {source} failed.")

        return documents[0]
