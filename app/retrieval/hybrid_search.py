# retrieval/hybrid_search.py

from app.embeddings.bge_m3 import model
from app.vectordb.qdrant_client import COLLECTION_NAME, client
from config import settings


def retrieve(query):
    query_embedding = model.encode(
        [query],
        return_dense=True,
        return_sparse=True,
    )

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding["dense_vecs"][0],
        limit=settings.TOP_K_RETRIEVAL,
    )

    return results.points
