from main import generate_soap, clinical_decision

def test_generate_soap_structure():
    conversation = "Patient reports chest discomfort"
    soap = generate_soap(conversation)

    assert "assessment" in soap
    assert "confidence" in soap["assessment"]
    assert 0 <= soap["assessment"]["confidence"] <= 1


def test_clinical_decision_alert():
    assessment = {
        "risk_level": "high",
        "confidence": 0.9
    }

    decision = clinical_decision(assessment)

    assert decision["decision"] == "ALERT_DOCTOR"

def test_rag_retrieval_returns_guidelines():
    from retrieve_guidelines import retrieve

    results = retrieve("patient has chest pain")
    assert isinstance(results, list)
    assert len(results) > 0


def test_generate_soap_contract():
    conversation = "Patient reports chest pain"
    soap = generate_soap(conversation)

    assert "assessment" in soap
    assert "risk_level" in soap["assessment"]
    assert "confidence" in soap["assessment"]
    assert 0.0 <= soap["assessment"]["confidence"] <= 1.0

def test_decision_logic_never_crashes():
    assessment = {
        "risk_level": "unknown",
        "confidence": 0.5
    }

    decision = clinical_decision(assessment)
    assert "decision" in decision

def test_mock_mode_default(monkeypatch):
    monkeypatch.delenv("USE_REAL_LLM", raising=False)
    soap = generate_soap("test")
    assert soap["assessment"]["confidence"] == 0.9

