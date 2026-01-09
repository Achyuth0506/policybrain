"""
OnboardPro - Decision Logic Version
Simulates HR candidate matching and hiring decisions.
"""
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

def match_candidate(job: str, candidate: str) -> Dict:
    """
    Mock candidate-job matching result.
    """
    return {
        "fit_score": 72,
        "confidence": 0.85,
        "bias_check": {
            "used_protected_attributes": False
        }
    }


def hiring_decision(result: Dict) -> Dict:
    """
    Make hiring recommendation based on rules.
    """
    score = result["fit_score"]
    confidence = result["confidence"]
    bias_ok = not result["bias_check"]["used_protected_attributes"]

    if score >= 75 and confidence >= 0.8 and bias_ok:
        decision = "STRONG_INTERVIEW"
    elif score >= 60 and bias_ok:
        decision = "INTERVIEW"
    else:
        decision = "NO_INTERVIEW"

    return {
        "decision": decision,
        "reason": f"score={score}, confidence={confidence}, bias_ok={bias_ok}"
    }


if __name__ == "__main__":
    job = "Backend developer"
    candidate = "Python and API experience"

    result = match_candidate(job, candidate)
    decision = hiring_decision(result)

    audit_log("OnboardPro", f"{job} | {candidate}", {
        "match": result,
        "decision": decision
    })

    print("HIRING DECISION:", decision)


