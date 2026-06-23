# embeddings/bge_m3.py

from FlagEmbedding import BGEM3FlagModel

from config import settings

model = BGEM3FlagModel(
    settings.EMBEDDING_MODEL,
    use_fp16=True,
)


def warmup() -> None:
    """Prime the embedding model so the first real request is faster."""
    embed(["warmup"])


def embed(texts):
    output = model.encode(
        texts,
        return_dense=True,
        return_sparse=True,
        return_colbert_vecs=True,
    )
    return {
        "dense": output["dense_vecs"],
        "sparse": output["lexical_weights"],
        "colbert": output["colbert_vecs"],
    }
