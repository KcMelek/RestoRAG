# tests/scoring.py


def keyword_score(answer, expected_keywords):
    if not expected_keywords:
        return 1.0

    answer = (answer or "").lower()

    hits = 0
    for kw in expected_keywords:
        if kw.lower() in answer:
            hits += 1

    return hits / len(expected_keywords)


def action_correct(predicted, expected):
    if predicted in (None, "", "null"):
        predicted = None
    if expected in (None, "", "null"):
        expected = None
    if isinstance(expected, list):
        if isinstance(predicted, list):
            return sorted(predicted) == sorted(expected)
        return False
    return predicted == expected
