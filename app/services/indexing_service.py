"""
Document indexing service for DialAgent.
Single source of truth for: parse → chunk → embed → Qdrant.
Used by CLI, API, and Streamlit.
"""

import os
from typing import TypedDict

from qdrant_client.models import PointStruct

from app.chunking.semantic_chunker import create_chunks
from app.embeddings.bge_m3 import embed
from app.ingestion.document_parser import SUPPORTED_EXTENSIONS, parse_document
from app.ingestion.normalizer import normalize_text
from app.vectordb.qdrant_client import COLLECTION_NAME, DB_PATH, client, ensure_collection


class SourceStats(TypedDict):
    filename: str
    chunks: int


class IndexStats(TypedDict):
    total_chunks: int
    sources: list[SourceStats]
    db_path: str


def save_to_qdrant(chunks, embeddings, source_name: str, point_id_offset: int) -> int:
    """Save chunks with their embeddings to Qdrant vector store."""
    points = []

    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings["dense"])):
        sparse_dict = {k: float(v) for k, v in embeddings["sparse"][i].items()}
        point = PointStruct(
            id=point_id_offset + i,
            vector=embedding.tolist(),
            payload={
                "text": chunk.page_content,
                "source": source_name,
                "sparse": sparse_dict,
                "colbert": embeddings["colbert"][i].tolist(),
            },
        )
        points.append(point)

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )

    return point_id_offset + len(chunks)


def _next_point_offset() -> int:
    existing = client.count(collection_name=COLLECTION_NAME, exact=True)
    return existing.count if existing else 0


def index_markdown(
    markdown: str,
    source_name: str,
    point_id_offset: int | None = None,
) -> int:
    """Index normalized markdown text under a source filename. Returns chunk count."""
    ensure_collection(recreate=False)
    clean_text = normalize_text(markdown)
    chunks = create_chunks(clean_text)
    embeddings = embed([chunk.page_content for chunk in chunks])
    offset = _next_point_offset() if point_id_offset is None else point_id_offset
    save_to_qdrant(chunks, embeddings, source_name, offset)
    return len(chunks)


def index_file(
    file_path: str,
    force_ocr: bool | None = None,
    point_id_offset: int | None = None,
) -> dict:
    """Convert and index a local file. Returns ingestion summary."""
    source_name = os.path.basename(file_path)
    markdown = parse_document(file_path, force_ocr=force_ocr)
    chunks_indexed = index_markdown(markdown, source_name, point_id_offset=point_id_offset)
    return {
        "filename": source_name,
        "chunks_indexed": chunks_indexed,
        "char_count": len(markdown),
    }


def index_upload(
    filename: str,
    content: bytes,
    force_ocr: bool | None = None,
) -> dict:
    """Convert uploaded bytes and index them. Returns full ingestion summary."""
    from app.services.document_service import convert_upload_to_markdown

    result = convert_upload_to_markdown(filename, content, force_ocr=force_ocr)
    chunks_indexed = index_markdown(result["markdown"], result["filename"])
    return {
        "filename": result["filename"],
        "format": result["format"],
        "char_count": result["char_count"],
        "ocr_used": result["ocr_used"],
        "chunks_indexed": chunks_indexed,
    }


def ingest_directory(data_dir: str, recreate: bool = True) -> dict:
    """Ingest all supported documents from a directory into the vector store."""
    if not os.path.isdir(data_dir):
        raise FileNotFoundError(f"Directory not found: {data_dir}")

    ensure_collection(recreate=recreate)

    all_documents = [
        os.path.join(data_dir, f)
        for f in sorted(os.listdir(data_dir))
        if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS
    ]

    if not all_documents:
        return {"total_chunks": 0, "files": []}

    ingested_files = []
    total_chunks = 0
    next_offset = _next_point_offset()

    for file in all_documents:
        print(f"Processing {file}...")
        summary = index_file(file, point_id_offset=next_offset)
        total_chunks += summary["chunks_indexed"]
        next_offset += summary["chunks_indexed"]
        ingested_files.append(summary)
        print(
            f"Finished {summary['filename']} "
            f"({summary['chunks_indexed']} chunks, {summary['char_count']:,} chars)"
        )

    return {"total_chunks": total_chunks, "files": ingested_files}


def get_index_stats() -> IndexStats:
    """List indexed source files and chunk counts from the vector store."""
    collections = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in collections:
        return {"total_chunks": 0, "sources": [], "db_path": DB_PATH}

    source_counts: dict[str, int] = {}
    offset = None

    while True:
        records, offset = client.scroll(
            collection_name=COLLECTION_NAME,
            limit=100,
            offset=offset,
            with_payload=["source"],
            with_vectors=False,
        )
        for record in records:
            src = record.payload.get("source", "unknown")
            source_counts[src] = source_counts.get(src, 0) + 1
        if offset is None:
            break

    sources = [
        {"filename": name, "chunks": count}
        for name, count in sorted(source_counts.items())
    ]
    return {
        "total_chunks": sum(source_counts.values()),
        "sources": sources,
        "db_path": DB_PATH,
    }
