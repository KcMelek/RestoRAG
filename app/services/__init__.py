"""Application services shared by CLI, API, and Streamlit.

Import submodules directly to avoid loading heavy dependencies at package import time:
  from app.services.indexing_service import index_upload
  from app.services.rag_service import query_knowledge_base
"""

__all__ = [
    "document_service",
    "indexing_service",
    "rag_service",
]
