import logging

from llama_index.vector_stores import MilvusVectorStore
from pymilvus import Collection, CollectionSchema, FieldSchema, DataType, connections, utility

logger = logging.getLogger("knowledge_base.vector_store")

COLLECTION = "raggy"
VECTOR_DIM = 384
EMBEDDING_FIELD = "embedding"
DOC_ID_FIELD = "postgres_doc_id"
ALIAS = "default"


def initialize_milvus_store(uri: str, load_collection: bool = False):
    # Connect to the Milvus server
    connections.connect(alias=ALIAS, uri=uri)

    create_milvus_collection()

    # Llamaindex wrapper
    milvus_store = MilvusVectorStore(
        uri=uri,
        collection_name=COLLECTION,
        dim=VECTOR_DIM,
        embedding_field=EMBEDDING_FIELD,
        doc_id_field=DOC_ID_FIELD,
    )

    # Ensure collection is loaded
    milvus_store.collection.load()

    return milvus_store


def create_milvus_collection():
    # Check if the collection already exists
    if utility.has_collection(COLLECTION):
        logger.info(F"Collection '{COLLECTION}' already exists.")
        return

    # Define the fields for the collection
    fields = [
        FieldSchema(name=DOC_ID_FIELD, dtype=DataType.INT64, is_primary=True, auto_id=False),
        FieldSchema(name="user_id", dtype=DataType.INT64),
        FieldSchema(name="document_title", dtype=DataType.VARCHAR, max_length=1024),
        FieldSchema(name="doc_id", dtype=DataType.VARCHAR, max_length=2048),
        FieldSchema(name="id", dtype=DataType.VARCHAR, max_length=255),

        FieldSchema(name=EMBEDDING_FIELD, dtype=DataType.FLOAT_VECTOR, dim=VECTOR_DIM)
    ]

    # Create the collection schema
    schema = CollectionSchema(fields=fields, description=f"Collection for storing {COLLECTION} document embeddings and metadata", enable_dynamic_field=True)

    # Create the collection
    collection = Collection(name=COLLECTION, schema=schema)

    logger.info(f"Collection '{COLLECTION}' created successfully.")

    # Create the index
    index_params = {
        "index_type": "IVF_FLAT",
        "metric_type": "L2",
        "params": {"nlist": 128},
    }
    collection.create_index(field_name="embedding", index_params=index_params)

    logger.info(f"Index for collection '{COLLECTION}' created successfully.")