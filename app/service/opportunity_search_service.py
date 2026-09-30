from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.schema.opportunity_search import (
    OpportunitySearchCreate,
    OpportunitySearchResponse,
    OpportunitySearchStatus,
)

from app.repository.opportunity_search_repo import (
    InMemoryOpportunitySearchRepository,
)


class OpportunitySearchService:
    def __init__(
        self,
        repositoy: InMemoryOpportunitySearchRepository,
    ) -> None:
        self._repository = repositoy

    def create(
        self,
        request: OpportunitySearchCreate,
    ) -> OpportunitySearchResponse:
        search = OpportunitySearchResponse(
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
    
        return self._repository.save(search)

    def get_by_id(
            self,
            search_id: UUID,
    ) -> OpportunitySearchResponse | None:
        return self._repository.get_by_id(search_id)
        
        