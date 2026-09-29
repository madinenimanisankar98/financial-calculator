"""
Ask Questions AI assistant.

Tries the Gemini API if GEMINI_API_KEY is set in the environment; otherwise
falls back to a small offline knowledge base so the feature still works
with zero configuration (important for a college demo / grading run).
"""

import os
import re

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-1.5-flash:generateContent"
)

SYSTEM_PROMPT = (
    "You are a friendly financial literacy assistant inside a student's "
    "Financial Calculator app. Answer questions about savings, loans/EMI, "
    "GST, and budgeting in simple, encouraging language. Keep answers under "
    "120 words. If asked something unrelated to personal finance, gently "
    "steer the conversation back."
)

# --- Offline fallback knowledge base -------------------------------------

_OFFLINE_KB = [
    (r"\bemi\b|\bloan\b|\binterest rate\b",
     "EMI (Equated Monthly Installment) is the fixed amount you pay each "
     "month toward a loan. It covers both principal and interest. A longer "
     "tenure lowers your EMI but increases total interest paid — a shorter "
     "tenure does the opposite."),
    (r"\bsav(e|ing|ings)\b|\bbudget\b",
     "A simple rule of thumb: try to save at least 20% of your income. "
     "Track your monthly income and expenses first — the gap between them "
     "is what you can actually save or invest."),
    (r"\bgst\b|\btax\b",
     "GST (Goods and Services Tax) is added to the price of most goods and "
     "services in India. Common slabs are 5%, 12%, 18%, and 28%. 'Exclusive' "
     "means GST is added on top of the price; 'inclusive' means it's already "
     "built in."),
    (r"\bpercent|%",
     "To find a percentage of a number: multiply the number by the "
     "percentage and divide by 100. For example, 15% of 800 is (800×15)/100 "
     "= 120."),
    (r"\bcompound interest\b",
     "Compound interest means you earn (or owe) interest on both your "
     "original amount and on interest already added. Over long periods, it "
     "grows much faster than simple interest."),
]

_DEFAULT_REPLY = (
    "I can help with savings goals, EMI/loans, GST, and percentages. Try "
    "asking something like 'How is EMI calculated?' or 'What does GST "
    "inclusive mean?'"
)


def _offline_answer(question):
    q = question.lower()
    for pattern, answer in _OFFLINE_KB:
        if re.search(pattern, q):
            return answer
    return _DEFAULT_REPLY


def _gemini_answer(question):
    """Call the Gemini API. Returns None on any failure so the caller can fall back."""
    if not GEMINI_API_KEY:
        return None
    try:
        import requests  # imported here so the app still runs without `requests`
        resp = requests.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            json={
                "contents": [{"parts": [{"text": question}]}],
                "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
            },
            timeout=8,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception:
        return None


def answer_question(question):
    """
    Public entry point used by the /api/ask-ai route.
    Tries Gemini first (if configured), falls back to the offline KB.
    """
    if not question or not question.strip():
        return {"answer": _DEFAULT_REPLY, "source": "offline"}

    gemini_reply = _gemini_answer(question)
    if gemini_reply:
        return {"answer": gemini_reply, "source": "gemini"}

    return {"answer": _offline_answer(question), "source": "offline"}
