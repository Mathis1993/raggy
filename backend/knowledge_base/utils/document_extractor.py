from pathlib import Path

from llama_index import download_loader
from llama_index.readers import BeautifulSoupWebReader


class DocumentExtractor:
    @staticmethod
    def extract_content_from_url(url: str):
        documents = BeautifulSoupWebReader().load_data([url])
        if len(documents) == 0:
            raise ValueError(f"Content extraction from url {url} failed.")
        document = documents[0]
        return document

    @staticmethod
    def extract_content_from_pdf(file_path: str):
        PDFReader = download_loader("PDFReader")
        loader = PDFReader()
        documents = loader.load_data(file=Path(file_path))
        if len(documents) == 0:
            raise ValueError(f"Content extraction from pdf {file_path} failed.")
        return documents[0]
