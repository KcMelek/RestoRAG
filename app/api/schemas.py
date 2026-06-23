"""Pydantic request/response models for the FastAPI layer."""

from pydantic import BaseModel


class ConvertPathRequest(BaseModel):
    path: str
    force_ocr: bool | None = None


class QueryRequest(BaseModel):
    query: str


class ConvertResponse(BaseModel):
    filename: str
    format: str
    markdown: str
    char_count: int
    ocr_used: bool


class QueryResponse(BaseModel):
    answer: str
    action: str | None = None


class SourceStatsResponse(BaseModel):
    filename: str
    chunks: int


class IndexStatsResponse(BaseModel):
    total_chunks: int
    sources: list[SourceStatsResponse]
    db_path: str


class IndexUploadResponse(BaseModel):
    filename: str
    format: str
    char_count: int
    ocr_used: bool
    chunks_indexed: int
