from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from app.repository.sqlalchemy_evidence_repo import (
    SqlAlchemyEvidenceRepository,
)
from app.repository.sqlalchemy_opportunity_search_repo import (
    SqlAlchemyOpportunitySearchRepository,
)
from app.schema.evidence import EvidenceResponse
from app.schema.opportunity_search import (
    OpportunitySearchResponse,
    OpportunitySearchStatus,
)


def test_save_and_retrieve_evidence(
    db_session: Session,
) -> None:
    search_repository = SqlAlchemyOpportunitySearchRepository(
        db_session,
    )
    evidence_repository = SqlAlchemyEvidenceRepository(
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
            "Identify an unmet customer need for a new product"
        ),
        constraints=["Retail price below $60"],
        initial_hypothesis=None,
        status=OpportunitySearchStatus.CREATED,
        created_at=datetime.now(UTC),
    )

    search_repository.save(search)

    evidence = EvidenceResponse(
        id=uuid4(),
        opportunity_search_id=search.id,
        source_type="customer_review",
        source_name="Amazon review",
        content=(
            "The moisturizer works well, but the packaging "
            "creates too much waste."
        ),
        source_url="https://example.com/reviews/123",
        created_at=datetime.now(UTC),
    )

    saved_evidence = evidence_repository.save(evidence)
    retrieved_evidence = evidence_repository.get_by_id(
        evidence.id,
    )

    assert saved_evidence == evidence
    assert retrieved_evidence == evidence