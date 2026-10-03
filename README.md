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

- Creating and retrieving opportunity searches
- Validating request and response data with Pydantic
- Assigning UUIDs, lifecycle status, and UTC timestamps
- Persisting searches in PostgreSQL through SQLAlchemy
- Managing schema changes with Alembic migrations
- Returning `404 Not Found` for unknown searches
- Isolated unit and PostgreSQL integration tests
- Rolling back database changes after each automated test

## Current Architecture

```text
FastAPI route
    ↓
OpportunitySearchService
    ↓
OpportunitySearchRepository Protocol
    ↓
SQLAlchemy repository
    ↓
PostgreSQL
```

The repository boundary also supports an in-memory implementation for focused unit tests. FastAPI dependency injection creates a request-scoped SQLAlchemy session, repository, and service.

## Technology Stack

### Current

- Python
- FastAPI
- Pydantic
- Pytest
- HTTPX/FastAPI TestClient
- SQLAlchemy 2.x
- PostgreSQL 17
- Psycopg
- Alembic
- Docker Compose

### Planned

- pgvector
- LLM tool calling and structured outputs
- Retrieval-augmented generation
- Evaluation harnesses
- Observability and tracing
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

### 4. Start PostgreSQL

```bash
docker compose up -d
```

### 5. Apply database migrations

```bash
alembic upgrade head
```

### 6. Start the API

```bash
uvicorn app.main:app --reload
```

Then open:

- API documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Health endpoint: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

## Running the Tests

Create the dedicated test database once:

```bash
docker compose exec postgres createdb \
  -U opportunity_user \
  product_opportunity_test
```

Apply migrations to it:

```bash
DATABASE_URL="postgresql+psycopg://opportunity_user:opportunity_password@localhost:5433/product_opportunity_test" \
alembic upgrade head
```

Run the tests:

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
- In-memory repository unit behavior
- SQLAlchemy repository integration
- Persisted API behavior
- Per-test transaction rollback and database isolation

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
- [x] PostgreSQL persistence with SQLAlchemy
- [x] Database migrations with Alembic
- [x] Isolated PostgreSQL integration tests
- [x] Docker Compose for local PostgreSQL
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
- [ ] Containerized application deployment

## Project Status

This project is being developed incrementally as a production-oriented applied AI portfolio project. Architecture, tests, persistence, retrieval, agent orchestration, evaluation, and observability are being added in stages.