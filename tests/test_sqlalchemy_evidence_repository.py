from datetime import UTC, datetime
from uuid import uuid4

import pytest

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

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
from app.schema.evidence_chunk import EvidenceChunkResponse

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


def test_save_evidence_with_chunks(
    db_session: Session,
) -> None:
    search_repository = SqlAlchemyOpportunitySearchRepository(
        db_session,
    )
    evidence_repository = SqlAlchemyEvidenceRepository(
        db_session,
    )
    now = datetime.now(UTC)

    search = OpportunitySearchResponse(
        id=uuid4(),
        product_category="Facial moisturizer",
        market="United States",
        target_customer="Consumers with sensitive skin",
        objective="Identify unmet skincare needs",
        constraints=[],
        initial_hypothesis=None,
        status=OpportunitySearchStatus.CREATED,
        created_at=now,
    )
    search_repository.save(search)

    evidence = EvidenceResponse(
        id=uuid4(),
        opportunity_search_id=search.id,
        source_type="document",
        source_name="feedback.txt",
        content="Customers want less packaging and lower prices.",
        source_url=None,
        created_at=now,
    )

    chunk0 = EvidenceChunkResponse(
        id=uuid4(),
        evidence_id=evidence.id,
        chunk_index=0,
        content="Customers want less packaging",
        created_at=now,
    )
    chunk1 = EvidenceChunkResponse(
        id=uuid4(),
        evidence_id=evidence.id,
        chunk_index=1,
        content="and lower prices.",
        created_at=now,
    )

    saved_evidence = evidence_repository.save_with_chunks(
        evidence,
        [chunk1, chunk0],
    )

    db_session.expunge_all()

    assert saved_evidence == evidence
    assert evidence_repository.get_by_id(evidence.id) == evidence
    assert evidence_repository.find_chunks_by_evidence_id(
        evidence.id,
    ) == [chunk0, chunk1]
    assert evidence_repository.find_chunks_by_evidence_id(
        uuid4(),
    ) == []


def test_chunk_failure_rolls_back_evidence(
    db_session: Session,
) -> None:
    search_repository = SqlAlchemyOpportunitySearchRepository(
        db_session,
    )
    evidence_repository = SqlAlchemyEvidenceRepository(
        db_session,
    )
    now = datetime.now(UTC)

    search = OpportunitySearchResponse(
        id=uuid4(),
        product_category="Facial moisturizer",
        market="United States",
        target_customer="Consumers with sensitive skin",
        objective="Identify unmet skincare needs",
        constraints=[],
        initial_hypothesis=None,
        status=OpportunitySearchStatus.CREATED,
        created_at=now,
    )
    search_repository.save(search)

    evidence = EvidenceResponse(
        id=uuid4(),
        opportunity_search_id=search.id,
        source_type="document",
        source_name="feedback.txt",
        content="Customers want less packaging and lower prices.",
        source_url=None,
        created_at=now,
    )

    chunk0 = EvidenceChunkResponse(
        id=uuid4(),
        evidence_id=evidence.id,
        chunk_index=0,
        content="Customers want less packaging",
        created_at=now,
    )
    chunk1 = EvidenceChunkResponse(
        id=uuid4(),
        evidence_id=evidence.id,
        chunk_index=0,
        content="and lower prices.",
        created_at=now,
    )

    with pytest.raises(IntegrityError):
        evidence_repository.save_with_chunks(
            evidence,
            [chunk0, chunk1],
        )

    db_session.expunge_all()

    assert evidence_repository.get_by_id(evidence.id) is None
    assert evidence_repository.find_chunks_by_evidence_id(
        evidence.id,
    ) == []

    assert search_repository.get_by_id(search.id) == search