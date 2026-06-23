# ingestion/document_parser.py

from pathlib import Path

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import EasyOcrOptions, PdfPipelineOptions
from docling.document_converter import (
    DocumentConverter,
    ImageFormatOption,
    PdfFormatOption,
    WordFormatOption,
)

from config import settings

IMAGE_EXTENSIONS = settings.IMAGE_EXTENSIONS
SUPPORTED_EXTENSIONS = set(settings.SUPPORTED_EXTENSIONS)

_converters: dict[bool, DocumentConverter] = {}


def _build_pipeline_options(do_ocr: bool) -> PdfPipelineOptions:
    opts = PdfPipelineOptions(
        do_ocr=do_ocr,
        do_table_structure=True,
        images_scale=settings.OCR_IMAGES_SCALE,
    )
    if do_ocr:
        opts.ocr_options = EasyOcrOptions(lang=settings.OCR_LANGUAGES)
    return opts


def _get_converter(do_ocr: bool) -> DocumentConverter:
    if do_ocr not in _converters:
        pipeline_options = _build_pipeline_options(do_ocr)
        _converters[do_ocr] = DocumentConverter(
            allowed_formats=[
                InputFormat.PDF,
                InputFormat.IMAGE,
                InputFormat.DOCX,
            ],
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options),
                InputFormat.IMAGE: ImageFormatOption(pipeline_options=pipeline_options),
                InputFormat.DOCX: WordFormatOption(),
            },
        )
    return _converters[do_ocr]


def warmup() -> None:
    """Build both OCR and non-OCR converter variants during app startup."""
    _get_converter(False)
    _get_converter(True)


def _resolve_ocr(file_path: Path, force_ocr: bool | None) -> bool:
    if force_ocr is not None:
        return force_ocr
    if file_path.suffix.lower() in IMAGE_EXTENSIONS:
        return True
    return settings.DO_OCR


def parse_document(file_path: str, force_ocr: bool | None = None) -> str:
    """
    Convert a supported document to markdown.

    Supports PDF, Word (.docx), images (menu photos, multi-page scans),
    and plain markdown files. Images always use OCR; PDFs follow settings.DO_OCR.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = path.suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        raise ValueError(f"Unsupported file type '{ext}'. Supported: {supported}")

    if ext == ".md":
        return path.read_text(encoding="utf-8")

    do_ocr = _resolve_ocr(path, force_ocr)
    converter = _get_converter(do_ocr)
    result = converter.convert(str(path))
    return result.document.export_to_markdown()
