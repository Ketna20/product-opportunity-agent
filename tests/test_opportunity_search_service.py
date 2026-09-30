from uuid import UUID

from app.schema.opportunity_search import (
    OpportunitySearchCreate,
    OpportunitySearchStatus,
)
from app.service.opportunity_search_service import OpportunitySearchService
from app.repository.opportunity_search_repo import InMemoryOpportunitySearchRepository

def test_create_opportunity_search() -> None:
    repository = InMemoryOpportunitySearchRepository()
    service = OpportunitySearchService(repository)

    request = OpportunitySearchCreate(
        product_category="Facial moisturizer",
        market="United States",
        target_customer=(
            "Environmentally conscious skincare consumers"
        ),
        objective=(
            "Identify an unmet customer need that could "
            "support a new product"
        ),
        constraints=[
            "Retail price below $60",
            "Suitable for direct-to-consumer sales",
        ],
        initial_hypothesis=None,
    )

    result = service.create(request)

    stored_search = repository.get_by_id(result.id)

    assert isinstance(result.id, UUID)
    assert stored_search == result
    retrieved_Search= service.get_by_id(result.id)
    assert retrieved_Search == result
    assert result.product_category == request.product_category
    assert result.market == request.market
    assert result.target_customer == request.target_customer
    assert result.objective == request.objective
    assert result.constraints == request.constraints
    assert result.initial_hypothesis is None
    assert result.status == OpportunitySearchStatus.CREATED
    assert result.created_at.tzinfo is not None