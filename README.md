# AI Agent Systems — Production-Style Portfolio

This repository contains two production-style AI backend systems designed
with safety, structure, and scalability in mind.

Both systems use real LLMs responsibly, with strict output contracts,
retrieval-augmented generation (RAG), decision logic, audit logging,
automated testing, and containerized deployment.

---

## 📌 Projects

### 🏥 CliniDoc — Healthcare Documentation & Alerting
**Purpose:**  
Assist clinicians by converting conversations into structured SOAP-style
assessments and generating risk-aware alerts.

**Key Features:**
- Retrieval-Augmented Generation (FAISS vector search)
- Structured JSON outputs (no free-text risk)
- Rule-based clinical decision thresholds
- Audit logging for compliance
- Mock-first, feature-flagged real LLM usage
- FastAPI service with Docker deployment

📂 `clinidoc/`

---

### 👥 OnboardPro — HR Candidate Matching
**Purpose:**  
Support HR teams by matching candidates to job roles in a bias-aware,
auditable manner.

**Key Features:**
- Structured candidate–job evaluation
- Bias-safety checks
- Rule-based hiring recommendations
- Audit logging
- Automated tests
- FastAPI service with Docker deployment

📂 `onboardpro/`

---

## 🧠 Engineering Principles Demonstrated

- Separation of AI reasoning and business decisions
- Retrieval-based grounding to prevent hallucinations
- Strict schema enforcement for LLM outputs
- Cost and latency controls
- Feature-flagged rollout and rollback
- Test-driven confidence in AI behavior

---

## 🛠 Tech Stack

- Python 3.12
- OpenAI API
- FAISS (Vector Search)
- FastAPI
- Pytest
- Docker

---

## 🚀 How to Run (Example)

```bash
docker build -t clinidoc ./clinidoc
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_key_here \
  -e USE_REAL_LLM=true \
  clinidoc

# CliniDoc

CliniDoc is a healthcare AI backend designed to safely assist with clinical
documentation and alerting.

## What It Does
- Analyzes clinician–patient conversations
- Retrieves relevant medical guidelines using vector search (FAISS)
- Produces structured assessments
- Applies rule-based alert thresholds
- Logs every decision for auditability

## Safety Design
- AI does NOT diagnose
- Decisions are rule-based
- Outputs are strictly structured
- Mock mode is the default

## Run Locally

```bash
export USE_REAL_LLM=true
export OPENAI_API_KEY=your_key_here
python3 main.py


## Run as API

uvicorn api:app --reload

# OnboardPro

OnboardPro is an HR-focused AI backend that assists with candidate matching
while enforcing fairness and auditability.

## What It Does
- Evaluates job descriptions and candidate profiles
- Produces structured match scores
- Enforces bias-safety checks
- Generates hiring recommendations
- Logs all decisions

## Design Principles
- AI supports decisions, never replaces them
- No protected attributes are used
- Fully test-covered logic

## Run as API

```bash
uvicorn api:app --reload --port 8001

