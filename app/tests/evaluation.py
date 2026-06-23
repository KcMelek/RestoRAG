# tests/evaluation.py

from app.orchestration.rag_pipeline import answer
from app.tests.scoring import action_correct, keyword_score
from app.tests.test_cases import TEST_CASES


def run_evaluation():
    total = len(TEST_CASES)
    passed = 0
    results = []

    for tc in TEST_CASES:
        response = answer(tc["query"])

        score = keyword_score(
            response.get("answer", ""),
            tc["expected_answer_keywords"],
        )

        action_ok = action_correct(
            response.get("action"),
            tc["expected_action"],
        )

        success = score >= 0.8 and action_ok

        if success:
            passed += 1

        results.append(
            {
                "id": tc["id"],
                "query": tc["query"],
                "answer": response.get("answer", ""),
                "action": response.get("action"),
                "expected_keywords": tc["expected_answer_keywords"],
                "expected_action": tc["expected_action"],
                "score": round(score, 2),
                "action_ok": action_ok,
                "passed": success,
            }
        )

    accuracy = passed / total

    return {
        "accuracy": accuracy,
        "passed": passed,
        "total": total,
        "results": results,
    }
