# config.py

import os


class Settings:
    COLLECTION_NAME = "le_chateau_bistro"
    EMBEDDING_MODEL = "BAAI/bge-m3"
    RERANK_MODEL = "BAAI/bge-reranker-v2-m3"
    TOP_K_RETRIEVAL = 20
    TOP_K_RERANK = 5
    FINAL_CONTEXT_DOCS = 5

    # Document conversion
    DO_OCR = True
    OCR_LANGUAGES = ["fr", "en"]
    OCR_IMAGES_SCALE = 2.0

    SUPPORTED_EXTENSIONS = [
        ".pdf",
        ".docx",
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
        ".bmp",
        ".tiff",
        ".tif",
        ".md",
    ]

    IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".tif"}

    # Single local vector store path (override with QDRANT_PATH env var)
    QDRANT_PATH = os.getenv("QDRANT_PATH", "./qdrant_db")

    DEFAULT_INGEST_PATH = "data/raw"


settings = Settings()
