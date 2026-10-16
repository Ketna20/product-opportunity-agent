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


def test_find_evidence_by_opportunity_search_id(
    db_session: Session,
) -> None:
    search_repository = SqlAlchemyOpportunitySearchRepository(
        db_session,
    )
    evidence_repository = SqlAlchemyEvidenceRepository(
        db_session,
    )

    opportunity_search1 = OpportunitySearchResponse(
        id=uuid4(),
        product_category="Facial moisturizer",
        market="United States",
        target_customer=(
            "Consumers looking for better quality skincare products"
        ),
        objective=(
            "Identify an unmet customer need for a new product"
        ),
        constraints=["Suitable for sensitive skin"],
        initial_hypothesis=None,
        status=OpportunitySearchStatus.CREATED,
        created_at=datetime.now(UTC),
    )
    search_repository.save(opportunity_search1)

    opportunity_search2 = OpportunitySearchResponse(
        id=uuid4(),
        product_category="Facial moisturizer",
        market="United States",
        target_customer=(
            "Environmentally conscious skincare consumers"
        ),
        objective=(
            "Product performance"
        ),
        constraints=["Retail price below $60"],
        initial_hypothesis=None,
        status=OpportunitySearchStatus.CREATED,
        created_at=datetime.now(UTC),
    )
    search_repository.save(opportunity_search2)

    evidence1 = EvidenceResponse(
        id=uuid4(),
        opportunity_search_id=opportunity_search1.id,
        source_type="customer_review",
        source_name="Amazon review",
        content=(
            "The moisturizer works well, but the packaging "
            "creates too much waste."
        ),
        source_url="https://example.com/reviews/123",
        created_at=datetime.now(UTC),
    )
    saved_evidence1 = evidence_repository.save(evidence1)
    evidence2 = EvidenceResponse(
        id=uuid4(),
        opportunity_search_id=opportunity_search1.id,
        source_type="customer_review",
        source_name="Google review",
        content=(
            "The moisturizer does not irritate my sensitive skin, but it is too expensive."
        ),
        source_url="https://google.com/reviews/123",
        created_at=datetime.now(UTC),
    )
    saved_evidence2 = evidence_repository.save(evidence2)
    evidence3 = EvidenceResponse(
        id=uuid4(),
        opportunity_search_id=opportunity_search2.id,
        source_type="customer_review",
        source_name="Google review",
        content=(
            "The moisturizer is too greasy."
    ),
        source_url="https://google.com/reviews/123",
        created_at=datetime.now(UTC),
    )
    saved_evidence3 = evidence_repository.save(evidence3)
    retrieved_evidence1 = evidence_repository.find_by_opportunity_search_id(
        opportunity_search1.id,
    )

    assert retrieved_evidence1 == [
        saved_evidence1,
        saved_evidence2,
    ]
