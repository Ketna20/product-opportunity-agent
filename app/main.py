from uuid import UUID

from fastapi import FastAPI, HTTPException, status

from app.repository.opportunity_search_repo import (
    InMemoryOpportunitySearchRepository,
)
from app.schema.opportunity_search import (
    OpportunitySearchCreate,
    OpportunitySearchResponse,
)
from app.service.opportunity_search_service import (
    OpportunitySearchService,
)


app = FastAPI(
    title="Evidence-Grounded Product Opportunity Agent",
    description=(
        "Identifies product opportunities and connects them "
        "to supporting and contradictory evidence"
    ),
    version="0.1.0",
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


@app.get(
    "/opportunity-searches/{search_id}",
    response_model=OpportunitySearchResponse,
)
def get_opportunity_search(
    search_id: UUID,
) -> OpportunitySearchResponse:
    search = opportunity_search_service.get_by_id(search_id)
    if search is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunity search not found",
        )
    return search