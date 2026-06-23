"""Startup warmup helpers for the API and other long-lived processes."""

from app.embeddings.bge_m3 import warmup as warmup_embeddings
from app.ingestion.document_parser import warmup as warmup_parsers
from app.retrieval.reranker import warmup as warmup_reranker
from app.vectordb.qdrant_client import ensure_collection


def warmup_runtime() -> None:
    """Load the heavy runtime pieces before serving requests."""
    ensure_collection(recreate=False)
    warmup_parsers()
    warmup_embeddings()
    warmup_reranker()
