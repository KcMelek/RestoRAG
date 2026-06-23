# ingestion/pdf_loader.py — backward-compatible alias

from app.ingestion.document_parser import parse_document


def load_pdf(pdf_path: str) -> str:
    """Load a PDF and return markdown. Prefer parse_document() for new code."""
    return parse_document(pdf_path)
