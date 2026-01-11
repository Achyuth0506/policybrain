from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_valid_policy_question():
    response = client.post(
        "/query",
        json={"question": "Can patient data be stored in a public cloud under HIPAA?"}
    )

    assert response.status_code == 200
    data = response.json()

    assert "answer" in data
    assert "confidence" in data
    assert "citations" in data
    assert data["confidence"] >= 0.4
    assert len(data["citations"]) > 0


def test_unanswerable_question_refuses():
    response = client.post(
        "/query",
        json={"question": "Is patient data allowed on Mars?"}
    )

    assert response.status_code == 200
    data = response.json()

    assert data["confidence"] < 0.4
    assert data["citations"] == []
    assert "Insufficient information" in data["answer"]


def test_vague_question_low_confidence():
    response = client.post(
        "/query",
        json={"question": "Is cloud storage allowed?"}
    )

    assert response.status_code == 200
    data = response.json()

    assert data["confidence"] < 0.6

