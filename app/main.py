from datetime import UTC, datetime
from uuid import uuid4

from fastapi import FastAPI, status

from app.schema.opportunity_search import (
    OpportunitySearchCreate,
    OpportunitySearchResponse, 
    OpportunitySearchStatus,
)

app = FastAPI (
    title="Evidence-Grounded Product Opportunity Agent",
    description=(
        "Identifies product opportunities and connects them "
        "to supporting and contradictory evidence"
    ),
    version="0.1.0"
)

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}

@app.post(
    "/opportunity-searches",
    response_model=OpportunitySearchResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_opportunity_search(
    request: OpportunitySearchCreate,
) -> OpportunitySearchResponse:
    return OpportunitySearchResponse(
        id=uuid4(),
        product_category=request.product_category,
        market=request.market,
        target_customer=request.target_customer,
        objective=request.objective,
        constraints=request.constraints,
        initial_hypothesis=request.initial_hypothesis,
        status=OpportunitySearchStatus.CREATED,
        created_at=datetime.now(UTC),
    )