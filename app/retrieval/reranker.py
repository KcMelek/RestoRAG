# retrieval/reranker.py

from sentence_transformers import CrossEncoder

from config import settings

_reranker: CrossEncoder | None = None


def _get_reranker() -> CrossEncoder:
    global _reranker
    if _reranker is None:
        _reranker = CrossEncoder(settings.RERANK_MODEL)
    return _reranker


def warmup() -> None:
    """Load the reranker weights during startup instead of on first query."""
    _get_reranker()


def rerank(query, docs):
    if not docs:
        return []

    pairs = [[query, d.payload["text"]] for d in docs]
    scores = _get_reranker().predict(pairs)
    if not hasattr(scores, "__iter__"):
        scores = [scores]

    ranked = sorted(
        zip(docs, scores),
        key=lambda x: x[1],
        reverse=True,
    )

    return ranked[: settings.TOP_K_RERANK]
