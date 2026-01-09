"""
CliniDoc - Decision Logic Version
Adds alerting based on confidence and red flags.
"""
import os
import json
from retrieve_guidelines import retrieve
from openai import OpenAI
import json
from datetime import datetime, timezone
def audit_log(agent: str, input_data: str, output_data: dict):
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agent": agent,
        "input": input_data,
        "output": output_data
    }

    with open("audit_log.json", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

from typing import Dict

def retrieve_guidelines() -> str:
    with open("guidelines.txt") as f:
        return f.read()


def call_llm(prompt: str) -> dict:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY not set")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "system", "content": "You must return ONLY valid JSON."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.2,
    response_format={"type": "json_object"},
    timeout=15  
)


    content = response.choices[0].message.content
    if not content or not content.strip():
        raise RuntimeError("LLM returned empty response")

    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Invalid JSON from LLM: {content}") from e




def generate_soap(conversation: str) -> dict:
    use_real_llm = os.getenv("USE_REAL_LLM") == "true"

    if not use_real_llm:
        return {
            "assessment": {
                "summary": "Chest discomfort with fatigue",
                "risk_level": "high",
                "confidence": 0.9
            }
        }

    relevant_guidelines = retrieve(conversation)

    prompt = f"""
You are a clinical assistant.

Use ONLY the following clinical guidelines:
{relevant_guidelines}

Return ONLY valid JSON:
{{
  "assessment": {{
    "summary": "...",
    "risk_level": "low|medium|high",
    "confidence": 0.0-1.0
  }}
}}

Conversation:
{conversation}
"""

    
    MAX_PROMPT_LENGTH = 2000
    if len(prompt) > MAX_PROMPT_LENGTH:
        raise RuntimeError("Prompt too long — rejected to control cost")

    return call_llm(prompt)

            
                      

def clinical_decision(assessment: Dict) -> Dict:
    confidence = assessment["confidence"]
    risk = assessment["risk_level"]

    if risk == "high" and confidence >= 0.8:
        action = "ALERT_DOCTOR"
    elif risk == "medium" and confidence >= 0.6:
        action = "RECOMMEND_FOLLOW_UP"
    else:
        action = "NO_ACTION"

    return {
        "decision": action,
        "reason": f"Risk={risk}, confidence={confidence}"
    }


if __name__ == "__main__":
    conversation = "Patient reports chest discomfort and fatigue"

    soap = generate_soap(conversation)
    decision = clinical_decision(soap["assessment"])

    audit_log("CliniDoc", conversation, {
        "soap": soap,
        "decision": decision
    })

    print("DECISION:", decision)








