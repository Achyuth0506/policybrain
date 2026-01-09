from main import match_candidate, hiring_decision

def test_match_candidate_structure():
    result = match_candidate("Backend dev", "Python APIs")

    assert "fit_score" in result
    assert "confidence" in result
    assert 0 <= result["fit_score"] <= 100


def test_hiring_decision_logic():
    result = {
        "fit_score": 80,
        "confidence": 0.9,
        "bias_check": {
            "used_protected_attributes": False
        }
    }

    decision = hiring_decision(result)

    assert decision["decision"] == "STRONG_INTERVIEW"

