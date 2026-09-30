from fastapi import FastAPI, status

from app.schema.opportunity_search import (
    OpportunitySearchCreate,
    OpportunitySearchResponse,
    OpportunitySearchStatus,
)

from app.service.opportunity_search_service import OpportunitySearchService
from app.repository.opportunity_search_repo import InMemoryOpportunitySearchRepository

app = FastAPI(
    title="Data-Driven Product Opportunity Agent",
    description=(
        "Identifies product opportunities and connects them "
        "to supporting and contradictory evidence"
    ),
    version="0.1.0"
)

opportunity_search_repository = (
    InMemoryOpportunitySearchRepository()
)

opportunity_search_service = OpportunitySearchService(
    opportunity_search_repository
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
    return opportunity_search_service.create(request)