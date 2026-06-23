"""RAG query service — shared by CLI, API, and Streamlit."""


def query_knowledge_base(question: str) -> dict:
    """Run the full RAG pipeline for a user question."""
    from app.orchestration.rag_pipeline import answer

    return answer(question)
