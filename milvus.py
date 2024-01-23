import os

from dotenv import load_dotenv
from pymilvus import connections

if __name__ == "__main__":
    load_dotenv()
    # con_string = f"http://{os.getenv('MILVUS_USERNAME', 'root')}:{os.getenv('MILUVS_PASSWORD', 'Milvus')}@{os.getenv('MILVUS_HOST', 'localhost')}:{os.getenv('MILVUS_PORT',19530)}"
    con = connections.connect(
        alias="default",
        host=f"{os.getenv('MILVUS_HOST', 'localhost'):{os.getenv('MILVUS_PORT',19530)}}",
        token=f"{os.getenv('MILVUS_USERNAME', 'root')}:{os.getenv('MILVUS_PASSWORD', 'Milvus')}"
    )
    print(con)