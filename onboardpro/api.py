from fastapi import FastAPI
from pydantic import BaseModel
from main import match_candidate, hiring_decision

app = FastAPI(title="OnboardPro API")


class MatchInput(BaseModel):
    job: str
    candidate: str


@app.post("/onboardpro/match")
def match(job_input: MatchInput):
    result = match_candidate(job_input.job, job_input.candidate)
    decision = hiring_decision(result)

    return {
        "match_result": result,
        "decision": decision
    }

