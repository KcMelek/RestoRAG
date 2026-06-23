# vectordb/qdrant_client.py

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from config import settings

COLLECTION_NAME = settings.COLLECTION_NAME
VECTOR_SIZE = 1024
DB_PATH = settings.QDRANT_PATH

client = QdrantClient(path=DB_PATH)


def ensure_collection(recreate: bool = False) -> None:
    collections = [c.name for c in client.get_collections().collections]

    if COLLECTION_NAME in collections:
        if recreate:
            client.delete_collection(COLLECTION_NAME)
        else:
            return

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE,
        ),
    )
