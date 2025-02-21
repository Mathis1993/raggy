import logging
from typing import Optional

from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.vector_stores.milvus import MilvusVectorStore
from pymilvus import Collection, CollectionSchema, DataType, FieldSchema, connections, utility

from config import settings

logger = logging.getLogger(__name__)

class RaggyVectorStore:
    """Handler for vector store operations using Milvus."""

    COLLECTION_NAME = "raggy"
    VECTOR_DIM = 1536
    EMBEDDING_FIELD = "embedding"
    DOC_ID_FIELD = "postgres_doc_id"
    CONNECTION_ALIAS = "default"

    def __init__(self, host: str = settings.MILVUS_HOST, port: str = settings.MILVUS_PORT):
        """Initialize the vector store with connection details."""
        self.uri = f"http://{host}:{port}"
        self.store: Optional[MilvusVectorStore] = None
        self.index: Optional[VectorStoreIndex] = None
        self.connect()

    def connect(self) -> None:
        """Establish connection to Milvus server."""
        connections.connect(alias=self.CONNECTION_ALIAS, uri=self.uri)
        logger.info(f"Connected to Milvus server at {self.uri}")

    def _create_collection_if_not_exists(self) -> None:
        """Create Milvus collection with custom schema if it doesn't exist."""
        if utility.has_collection(self.COLLECTION_NAME):
            logger.info(f"Collection '{self.COLLECTION_NAME}' already exists.")
            return

        fields = [
            FieldSchema(
                name="id",
                dtype=DataType.VARCHAR,
                max_length=255,
                is_primary=True,
                auto_id=True,  # Let Milvus auto-generate a unique ID for each node
            ),
            FieldSchema(
                name="postgres_doc_id", dtype=DataType.INT64
            ),  # For filtering nodes by source document
            FieldSchema(name="user_id", dtype=DataType.INT64),
            FieldSchema(name="document_title", dtype=DataType.VARCHAR, max_length=1024),
            FieldSchema(name="doc_id", dtype=DataType.VARCHAR, max_length=2048),
            FieldSchema(
                name=self.EMBEDDING_FIELD,
                dtype=DataType.FLOAT_VECTOR,
                dim=self.VECTOR_DIM,
            ),
        ]

        schema = CollectionSchema(
            fields=fields,
            description=f"Collection for storing {self.COLLECTION_NAME} document embeddings and metadata",
            enable_dynamic_field=True,
        )

        collection = Collection(name=self.COLLECTION_NAME, schema=schema)
        logger.info(f"Collection '{self.COLLECTION_NAME}' created successfully.")

        index_params = {
            "index_type": "IVF_FLAT",
            "metric_type": "L2",
            "params": {"nlist": 128},
        }
        collection.create_index(field_name="embedding", index_params=index_params)
        logger.info(f"Index for collection '{self.COLLECTION_NAME}' created successfully.")

    def initialize_store(self, load_collection: bool = False) -> MilvusVectorStore:
        """Initialize the Milvus vector store with automatic collection creation."""
        self._create_collection_if_not_exists()

        self.store = MilvusVectorStore(
            uri=self.uri,
            collection_name=self.COLLECTION_NAME,
            dim=self.VECTOR_DIM,
            embedding_field=self.EMBEDDING_FIELD,
            doc_id_field=self.DOC_ID_FIELD,
        )

        if load_collection and self.store._collection:
            self.store._collection.load()

        return self.store

    def get_index(self) -> VectorStoreIndex:
        """Get or create the vector store index."""
        if not self.store:
            self.initialize_store(load_collection=True)

        self.index = VectorStoreIndex.from_vector_store(
            vector_store=self.store,
            storage_context=StorageContext.from_defaults(vector_store=self.store),
        )
        return self.index

# Create a singleton instance
vector_store = RaggyVectorStore()
vector_store.initialize_store(load_collection=True)
