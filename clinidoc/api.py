from fastapi import FastAPI
from pydantic import BaseModel
from main import generate_soap, clinical_decision

app = FastAPI(title="CliniDoc API")


class ConversationInput(BaseModel):
    conversation: str


@app.post("/clinidoc/analyze")
def analyze_conversation(input: ConversationInput):
    soap = generate_soap(input.conversation)
    decision = clinical_decision(soap["assessment"])

    return {
        "soap": soap,
        "decision": decision
    }

