# ingestion/docling_parser.py — backward-compatible alias

from app.ingestion.document_parser import parse_document


def parse_pdf(pdf_path: str) -> str:
    """Backward-compatible alias. Prefer parse_document() for new code."""
    return parse_document(pdf_path)
