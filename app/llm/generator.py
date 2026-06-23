# llm/generator.py

import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

SYSTEM_PROMPT = """
You are Le Chateau Bistro AI.

Rules:
1. Answer using ONLY the provided CONTEXT.
2. Never invent menu items, prices, staff names, or opening hours.
3. If the context contains relevant information, you MUST use it in your answer.
4. Say you don't know only when the context truly lacks the answer.
5. Always leave "action" as an empty string — the system sets actions separately.

Output JSON only:
{"answer": "", "action": ""}
"""

ESCALATION_GUIDANCE = {
    "refund_complaint": """
ESCALATION MODE: cold delivery / refund complaint.
Follow the Customer Conflict & Sentiment-Driven Escalation Protocols in CONTEXT.
Your answer MUST, in natural language:
- Say you are sorry for the cold delivery and how it impacted their dinner
- Acknowledge their frustration and refund request
- Explain you are transferring them to the on-duty manager right now to process the refund
""",
    "manager_escalation": """
ESCALATION MODE: customer needs a manager.
Apologize and explain you are transferring them to the on-duty manager now.
""",
}


def generate(
    question,
    context,
    escalation=None,
):
    system_prompt = SYSTEM_PROMPT
    if escalation:
        guidance = ESCALATION_GUIDANCE.get(escalation.get("type"), "")
        if guidance:
            system_prompt = f"{SYSTEM_PROMPT}\n{guidance}"

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": f"""
QUESTION:
{question}

CONTEXT:
{context}
"""
            }
        ]
    )

    return completion.choices[0].message.content