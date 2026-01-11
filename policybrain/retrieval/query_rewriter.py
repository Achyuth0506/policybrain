from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def rewrite_query(user_query: str) -> str:
    prompt = f"""
You rewrite healthcare compliance questions into formal policy search queries.

Rules:
- Do NOT answer the question
- Use formal regulatory language
- Expand abbreviations
- Be concise

User question:
{user_query}

Return only the rewritten query.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        timeout=10
    )

    return response.choices[0].message.content.strip()

