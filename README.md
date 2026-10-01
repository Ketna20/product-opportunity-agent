# Evidence-Grounded Product Opportunity Agent

An applied AI system designed to help product teams identify and evaluate unmet customer needs using internal and external evidence.

The long-term goal is to produce product-opportunity briefs that connect every major finding to supporting evidence, identify contradictions and assumptions, evaluate evidence strength, and support human review.

> This project is currently under active development.

## Why I’m Building It

Product teams often work with customer feedback, market research, support conversations, reviews, and internal documents spread across multiple systems.

This project explores how an AI agent can help teams:

- Retrieve relevant customer and market evidence
- Extract recurring needs and pain points
- Group related evidence
- Generate product-opportunity hypotheses
- Identify supporting and contradictory evidence
- Evaluate evidence strength
- Produce cited opportunity briefs
- Route results through human review

The focus is not only on generating AI output, but on making that output traceable, testable, and useful for product decisions.

## Current Capabilities

The current API supports:

- Creating an opportunity-search request
- Validating request data with Pydantic
- Assigning a UUID, lifecycle status, and UTC timestamp
- Storing searches in an in-memory repository
- Retrieving a search by ID
- Returning `404 Not Found` for an unknown search
- Automated API, service, and repository tests

## Current Architecture

```text
FastAPI route
    ↓
OpportunitySearchService
    ↓
InMemoryOpportunitySearchRepository
```

The application currently uses an in-memory repository. This boundary is intentionally separated so it can later be replaced with PostgreSQL through SQLAlchemy.

## Technology Stack

### Current

- Python
- FastAPI
- Pydantic
- Pytest
- HTTPX/FastAPI TestClient

### Planned

- SQLAlchemy
- PostgreSQL
- Alembic
- pgvector
- LLM tool calling and structured outputs
- Retrieval-augmented generation
- Evaluation harnesses
- Observability and tracing
- Docker
- Next.js and TypeScript

## API Endpoints

### Health check

```http
GET /health
```

### Create an opportunity search

```http
POST /opportunity-searches
```

Example request:

```json
{
  "product_category": "Facial moisturizer",
  "market": "United States",
  "target_customer": "Environmentally conscious skincare consumers",
  "objective": "Identify an unmet customer need that could support a new product",
  "constraints": [
    "Retail price below $60",
    "Suitable for direct-to-consumer sales"
  ],
  "initial_hypothesis": null
}
```

### Retrieve an opportunity search

```http
GET /opportunity-searches/{search_id}
```

## Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/Ketna20/product-opportunity-agent.git
cd product-opportunity-agent
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 4. Start the API

```bash
uvicorn app.main:app --reload
```

Then open:

- API documentation: `http://127.0.0.1:8000/docs`
- Health endpoint: `http://127.0.0.1:8000/health`

## Running the Tests

```bash
python -m pytest
```

The current test suite covers:

- Health-check behavior
- Opportunity-search creation
- Request validation
- Service-layer creation and retrieval
- Repository storage and retrieval
- Successful API retrieval
- `404 Not Found` behavior

## Project Structure

```text
product-opportunity-agent/
├── app/
│   ├── main.py
│   ├── repository/
│   │   └── opportunity_search_repo.py
│   ├── schema/
│   │   └── opportunity_search.py
│   └── service/
│       └── opportunity_search_service.py
├── tests/
│   ├── test_main.py
│   ├── test_opportunity_search_repository.py
│   └── test_opportunity_search_service.py
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Roadmap

- [x] FastAPI application foundation
- [x] Request and response validation
- [x] Service and repository boundaries
- [x] In-memory persistence
- [x] Create and retrieve endpoints
- [x] Automated tests
- [ ] PostgreSQL persistence with SQLAlchemy
- [ ] Database migrations with Alembic
- [ ] Evidence ingestion and document processing
- [ ] Semantic retrieval with embeddings and pgvector
- [ ] Evidence extraction and grouping
- [ ] Product-opportunity hypothesis generation
- [ ] Contradiction and assumption detection
- [ ] Evidence-strength evaluation
- [ ] Cited opportunity briefs
- [ ] Human review workflow
- [ ] Evaluation and observability
- [ ] Next.js user interface
- [ ] Docker and deployment

## Project Status

This project is being developed incrementally as a production-oriented applied AI portfolio project. Architecture, tests, persistence, retrieval, agent orchestration, evaluation, and observability are being added in stages.