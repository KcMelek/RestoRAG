# orchestration/guardrails.py

import re


def detect_escalation(query):
    q = query.lower()

    if (
        "refund" in q
        or "cold food" in q
        or ("delivery" in q and "cold" in q)
    ):
        return {
            "type": "refund_complaint",
            "action": [
                "IMMEDIATE_STAFF_SLACK_ALERT",
                "CALL_TRANSFER_BRIDGE",
            ],
        }

    if any(word in q for word in ["furious", "manager"]):
        return {
            "type": "manager_escalation",
            "action": "CALL_TRANSFER_BRIDGE",
        }

    return None


def detect_large_party(query):
    nums = re.findall(r"\d+", query)

    for n in nums:
        if int(n) > 8:
            return {
                "action": "CALL_TRANSFER_BRIDGE",
            }

    return None
