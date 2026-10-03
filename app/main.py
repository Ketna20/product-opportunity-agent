from typing import Annotated
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db_session

from app.repository.sqlalchemy_opportunity_search_repo import (
    SqlAlchemyOpportunitySearchRepository,
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

DatabaseSession = Annotated[
    Session,
    Depends(get_db_session),
]


def get_opportunity_search_service(
    session: DatabaseSession,
) -> OpportunitySearchService:
    repository = SqlAlchemyOpportunitySearchRepository(session)
    return OpportunitySearchService(repository)


OpportunitySearchServiceDependency = Annotated[
    OpportunitySearchService,
    Depends(get_opportunity_search_service),
]


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}


@app.post(
    "/opportunity-searches",
    status_code=status.HTTP_201_CREATED,
)
def create_opportunity_search(
    request: OpportunitySearchCreate,
    service: OpportunitySearchServiceDependency,
) -> OpportunitySearchResponse:
    return service.create(request)


@app.get(
    "/opportunity-searches/{search_id}",
)
def get_opportunity_search(
    search_id: UUID,
    service: OpportunitySearchServiceDependency,
) -> OpportunitySearchResponse:
    search = service.get_by_id(search_id)
    if search is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunity search not found",
        )
    return search