from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ingestion.index_builder import load_policy_chunks
from retrieval.multi_hop import multi_hop_retrieve
from reasoning.answer_generator import generate_answer

app = FastAPI(
    title="PolicyBrain API",
    description="Healthcare policy compliance RAG system",
    version="1.0"
)

# Load policy chunks once at startup
POLICY_CHUNKS = load_policy_chunks()


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    confidence: float
    citations: list[str]


@app.post("/query", response_model=QueryResponse)
def query_policy(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        evidence, multi_hop = multi_hop_retrieve(
            request.question, POLICY_CHUNKS
        )

        result = generate_answer(
            request.question, evidence, multi_hop
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal error while processing query"
        )

