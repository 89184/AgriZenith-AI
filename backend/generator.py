from groq import Groq
from backend.config import GROQ_API_KEY, GROQ_MODEL

_client = None

def get_groq_client():
    global _client
    if _client is None:
        _client = Groq(api_key=GROQ_API_KEY)
    return _client

def generate_answer(query, context):
    client = get_groq_client()
    if not context.strip():
        context = "No relevant documents were found."
    prompt = f"""
You are an agricultural expert.

RULES:
- Use ONLY the given context
- If context is insufficient, say so clearly
- Give practical, farmer-friendly advice
- Do NOT hallucinate facts

Context:
{context}

Question:
{query}

Answer:
"""
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful agricultural advisory assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=512
    )
    return response.choices[0].message.content.strip()