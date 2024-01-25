from typing import List

from llama_index import Document, VectorStoreIndex, StorageContext, ServiceContext
from llama_index.embeddings import LangchainEmbedding
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index.vector_stores import MilvusVectorStore


class DocumentIndex:
    def __init__(self, model_path: str = "sentence-transformers/all-MiniLM-L6-v2", collection_name: str = "test"):
        self.collection_name = collection_name
        self.embedding_model = LangchainEmbedding(HuggingFaceEmbeddings(model_name=model_path))
        self.storage_context = self._build_storage_context()
        self.service_context = self._build_service_context()

    def _build_storage_context(self):
        milvus_store = MilvusVectorStore(
            uri="http://localhost:19530",
            collection_name=self.collection_name,
        )
        storage_context = StorageContext.from_defaults(vector_store=milvus_store)
        return storage_context

    def _build_service_context(self):
        return ServiceContext.from_defaults(
            embed_model=self.embedding_model,
            chunk_size=128,
            chunk_overlap=15
        )

    def embed_texts(self, texts: List[str]):
        for text in texts:
            self.embed_text(text)

    def embed_text(self, text: str):
        doc = Document(text=text)
        index = VectorStoreIndex(
            storage_context=self.storage_context,
            service_context=self.service_context
        )
        index.insert(doc)

    def get_index(self):
        return VectorStoreIndex(
            storage_context=self.storage_context,
            service_context=self.service_context
        )
