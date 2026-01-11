from openai import OpenAI
import os
import json
from reasoning.confidence import calibrate_confidence

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_RULES = """
You are a healthcare policy assistant.

CRITICAL RULES:
- Respond with VALID JSON ONLY.
- Do NOT include markdown, explanations, or extra text.
- Do NOT wrap output in code blocks.
- Use ONLY the provided evidence.
- If evidence is insufficient, say so explicitly.
- Cite sources exactly as provided.
"""

def safe_json_parse(text: str) -> dict:
    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}") + 1

    if start != -1 and end != -1:
        try:
            return json.loads(text[start:end])
        except json.JSONDecodeError:
            pass

    raise ValueError("Invalid JSON from LLM")


def generate_answer(question: str, evidence_chunks: list, multi_hop_used: bool) -> dict:
    if not evidence_chunks:
        return {
            "answer": "Insufficient information to determine compliance.",
            "confidence": 0.1,
            "citations": []
        }

    evidence_text = "\n\n".join(
        f"[{c['source']}] {c['text']}" for c in evidence_chunks
    )

    prompt = f"""
Question:
{question}

Evidence:
{evidence_text}

Return JSON with keys:
- answer (string)
- confidence (number between 0 and 1)
- citations (list of sources)
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": SYSTEM_RULES},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            timeout=15
        )

        raw = response.choices[0].message.content
        result = safe_json_parse(raw)

        calibrated = calibrate_confidence(
             result.get("confidence", 0.5),
             evidence_chunks,
             multi_hop_used,
             question
        )
  

        result["confidence"] = calibrated

        if calibrated < 0.4:
            return {
                "answer": "Insufficient information to determine compliance.",
                "confidence": calibrated,
                "citations": []
            }

        return result

    except Exception:
        return {
            "answer": "Insufficient information to determine compliance.",
            "confidence": 0.1,
            "citations": []
        }

