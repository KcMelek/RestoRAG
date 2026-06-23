# services/document_service.py

import os
import tempfile
from pathlib import Path

from app.ingestion.document_parser import SUPPORTED_EXTENSIONS, parse_document
from config import settings


def convert_to_markdown(
    file_path: str,
    force_ocr: bool | None = None,
) -> dict:
    """Convert a local file to markdown. Primary entry point for CLI and API."""
    path = Path(file_path)
    markdown = parse_document(str(path), force_ocr=force_ocr)
    return {
        "filename": path.name,
        "format": path.suffix.lower(),
        "markdown": markdown,
        "char_count": len(markdown),
        "ocr_used": _ocr_used(path, force_ocr),
    }


def convert_upload_to_markdown(
    filename: str,
    content: bytes,
    force_ocr: bool | None = None,
) -> dict:
    """Convert uploaded file bytes to markdown (writes to a temp file for Docling)."""
    suffix = Path(filename).suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        raise ValueError(f"Unsupported file type '{suffix}'. Supported: {supported}")

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    try:
        result = convert_to_markdown(tmp_path, force_ocr=force_ocr)
        result["filename"] = Path(filename).name
        return result
    finally:
        os.unlink(tmp_path)


def list_supported_formats() -> list[str]:
    return sorted(settings.SUPPORTED_EXTENSIONS)


def _ocr_used(path: Path, force_ocr: bool | None) -> bool:
    if path.suffix.lower() == ".md":
        return False
    if path.suffix.lower() in settings.IMAGE_EXTENSIONS:
        return True if force_ocr is None else force_ocr
    if force_ocr is not None:
        return force_ocr
    return settings.DO_OCR
