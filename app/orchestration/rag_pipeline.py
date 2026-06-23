# orchestration/rag_pipeline.py

import json

from app.llm.generator import generate
from app.orchestration.context_builder import build_context
from app.orchestration.guardrails import detect_escalation, detect_large_party
from app.retrieval.hybrid_search import retrieve
from app.retrieval.reranker import rerank


def _retrieval_query(query, escalation):
    if escalation and escalation.get("type") == "refund_complaint":
        return (
            f"{query} customer conflict escalation protocol "
            "apology refund on-duty manager call transfer"
        )
    return query


def answer(query):
    escalation = detect_escalation(query)
    large_party = detect_large_party(query)

    search_query = _retrieval_query(query, escalation)
    docs = retrieve(search_query)
    docs = rerank(search_query, docs)
    context = build_context(docs)

    response = generate(query, context, escalation=escalation)
    if isinstance(response, str):
        response = json.loads(response)

    if escalation:
        response["action"] = escalation["action"]
    elif large_party:
        response["action"] = large_party["action"]

    response.setdefault("answer", "")
    response.setdefault("action", None)

    return response
