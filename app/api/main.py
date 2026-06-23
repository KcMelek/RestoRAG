# api/main.py — thin HTTP layer; business logic lives in app.services

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from app.api.schemas import (
    ConvertPathRequest,
    ConvertResponse,
    IndexStatsResponse,
    IndexUploadResponse,
    QueryRequest,
    QueryResponse,
)
from app.services.document_service import (
    convert_to_markdown,
    convert_upload_to_markdown,
    list_supported_formats,
)
from app.services.indexing_service import get_index_stats, index_upload
from app.services.runtime import warmup_runtime
from app.services.rag_service import query_knowledge_base


@asynccontextmanager
async def lifespan(_app: FastAPI):
    warmup_runtime()
    yield

app = FastAPI(
    title="DialAgent Document API",
    description="Convert PDF, Word, and image files to markdown; query the RAG knowledge base.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/formats")
def formats():
    return {"formats": list_supported_formats()}


@app.get("/index/stats", response_model=IndexStatsResponse)
def index_stats():
    """List files currently indexed in the vector store."""
    return get_index_stats()


@app.post("/convert", response_model=ConvertResponse)
async def convert_file(
    file: UploadFile = File(...),
    force_ocr: bool | None = Form(default=None),
):
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file")

    try:
        return convert_upload_to_markdown(
            filename=file.filename or "upload",
            content=content,
            force_ocr=force_ocr,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/convert/path", response_model=ConvertResponse)
def convert_path(body: ConvertPathRequest):
    if not os.path.isfile(body.path):
        raise HTTPException(status_code=404, detail=f"File not found: {body.path}")

    try:
        return convert_to_markdown(body.path, force_ocr=body.force_ocr)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/query", response_model=QueryResponse)
def query(body: QueryRequest):
    if not body.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    return query_knowledge_base(body.query)


@app.post("/convert-and-index", response_model=IndexUploadResponse)
async def convert_and_index(
    file: UploadFile = File(...),
    force_ocr: bool | None = Form(default=None),
):
    """Convert an uploaded file and immediately index it into the vector store."""
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file")

    try:
        return index_upload(
            filename=file.filename or "upload",
            content=content,
            force_ocr=force_ocr,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
