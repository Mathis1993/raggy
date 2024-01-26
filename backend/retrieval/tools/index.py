import logging
from typing import List

from llama_index import Document, VectorStoreIndex, StorageContext, ServiceContext
from llama_index.embeddings import LangchainEmbedding
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index.vector_stores import MilvusVectorStore


logger = logging.getLogger(__name__)


class DocumentIndex:
    def __init__(self, embedding_model_path: str = "sentence-transformers/all-MiniLM-L6-v2", collection_name: str = "test2"):
        self.collection_name = collection_name
        self.embedding_model_path = embedding_model_path
        self.index = self._build_index()
        logger.info("Initialized DocumentIndex")

    def _build_storage_context(self):
        milvus_store = MilvusVectorStore(
            uri="http://localhost:19530",
            collection_name=self.collection_name,
            dim=1536,
            doc_id_field="id",
        )
        print(milvus_store.collection_name)
        storage_context = StorageContext.from_defaults(vector_store=milvus_store)
        return storage_context

    def _build_service_context(self):
        embedding_model = LangchainEmbedding(HuggingFaceEmbeddings(model_name=self.embedding_model_path))
        return ServiceContext.from_defaults(
            embed_model=embedding_model,
            chunk_size=128,
            chunk_overlap=15
        )

    def insert_texts_into_index(self, texts: List[str]):
        for text in texts:
            self.insert_single_text_into_index(text)

    def insert_single_text_into_index(self, text: str):
        doc = Document(text=text)

        if self.index is None:
            self.index = self._build_index()

        # TODO: check if the document has already been indexed
        # if doc in self.index:
        #     logger.info(f"Document {doc} already in index")
        #     return

        self.index.insert(doc)
        self.index.storage_context.persist()

    def _build_index(self):
        storage_context = self._build_storage_context()
        return VectorStoreIndex.from_vector_store(
            vector_store=storage_context.vector_store,
        )
