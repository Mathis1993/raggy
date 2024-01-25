from typing import List

from llama_index import Document, VectorStoreIndex, StorageContext, ServiceContext
from llama_index.embeddings import LangchainEmbedding
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index.vector_stores import ChromaVectorStore
import chromadb


class DocumentEmbedder:
    def __init__(self, model_path: str = "sentence-transformers/all-MiniLM-L6-v2", collection_name: str = "test"):
        self.collection_name = collection_name
        self.embedding_model = LangchainEmbedding(HuggingFaceEmbeddings(model_name=model_path))
        self.storage_context = self._build_storage_context()
        self.service_context = self._build_service_context()

    def _build_storage_context(self):
        client = chromadb.PersistentClient()
        collection = client.get_or_create_collection(self.collection_name)
        vector_store = ChromaVectorStore(chroma_collection=collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        return storage_context

    def _build_service_context(self):
        return ServiceContext.from_defaults(embed_model=self.embedding_model)

    def embed(self, texts: List[str]):
        if not isinstance(texts, list):
            raise ValueError("Texts must be a list of strings")

        docs = [Document(text=text) for text in texts]
        index = VectorStoreIndex(
            storage_context=self.storage_context,
            service_context=self.service_context
        )
        for doc in docs:
            index.insert(doc)
