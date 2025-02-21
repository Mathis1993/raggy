from llama_index.core import Document, SimpleDirectoryReader
from .base import DocumentExtractor


class WordExtractor(DocumentExtractor):
    def extract(self, source: str) -> Document:
        reader = SimpleDirectoryReader(input_files=[source])
        documents = reader.load_data()

        if not documents:
            raise ValueError(f"Content extraction from Word document {source} failed.")

        return documents[0]
