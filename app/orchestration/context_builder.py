# orchestration/context_builder.py

from config import settings


def build_context(ranked_docs):
    context = ""

    for i, (doc, _score) in enumerate(ranked_docs[: settings.FINAL_CONTEXT_DOCS]):
        context += f"""
SOURCE {i + 1}
{doc.payload.get("source", "unknown")}

{doc.payload["text"]}

----------------------
"""

    return context
