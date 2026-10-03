from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from app.repository.sqlalchemy_opportunity_search_repo import (
    SqlAlchemyOpportunitySearchRepository,
)
from app.schema.opportunity_search import (
    OpportunitySearchResponse,
    OpportunitySearchStatus,
)


def test_save_and_retrieve_opportunity_search(
    db_session: Session,
) -> None:
    repository = SqlAlchemyOpportunitySearchRepository(
        db_session,
    )

    search = OpportunitySearchResponse(
        id=uuid4(),
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
        status=OpportunitySearchStatus.CREATED,
        created_at=datetime.now(UTC),
    )

    saved_search = repository.save(search)
    retrieved_search = repository.get_by_id(search.id)

    assert saved_search == search
    assert retrieved_search == search