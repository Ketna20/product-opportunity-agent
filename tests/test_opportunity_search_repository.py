from datetime import UTC, datetime
from uuid import uuid4

from app.repository.opportunity_search_repo import (
    InMemoryOpportunitySearchRepository,
)
from app.schema.opportunity_search import (
    OpportunitySearchResponse,
    OpportunitySearchStatus,
)
# Test for saving and retrieving an opportunity search
def test_saves_and_retrieves_opportunity_search() -> None:

    repository = InMemoryOpportunitySearchRepository()
    search_id = uuid4()
    search = OpportunitySearchResponse(
        id=search_id,
        product_category="Facial moisturizer",
        market="United States",
        target_customer="Environmentally conscious skincare consumers",
        objective="Identify an unmet customer need for a new product",
        constraints=["Retail price below $60"],
        initial_hypothesis=None,
        status=OpportunitySearchStatus.CREATED,
        created_at=datetime.now(UTC),
    )

    saved_search = repository.save(search)
    retrieved_search = repository.get_by_id(search_id)

    assert saved_search == search
    assert retrieved_search == search

# Test for retrieving a nonexistent opportunity search by ID
def test_returns_none_for_nonexistent_id() -> None:
    repository = InMemoryOpportunitySearchRepository()
    nonexistent_id = uuid4()

    retrieved_search = repository.get_by_id(nonexistent_id)
    assert retrieved_search is None

