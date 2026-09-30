from datetime import UTC, datetime
from uuid import uuid4

from app.schema.opportunity_search import (
    OpportunitySearchCreate,
    OpportunitySearchResponse,
    OpportunitySearchStatus,
)


class OpportunitySearchService:
    def create(
        self,
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