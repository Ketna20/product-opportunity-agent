import pytest
from uuid import UUID, uuid4

from app import service
from app.schema.evidence import (
    EvidenceCreate,
)

from app.service.evidence_service import EvidenceService
from app.repository.evidence_repo import InMemoryEvidenceRepository
from app.repository.opportunity_search_repo import (
    InMemoryOpportunitySearchRepository,
)
from app.schema.opportunity_search import OpportunitySearchCreate
from app.service.opportunity_search_service import (
    OpportunitySearchService,
)

from app.service.evidence_service import (
    EvidenceService,
    OpportunitySearchNotFoundError,
)


def test_create_evidence() -> None: 
    evidence_repository = InMemoryEvidenceRepository()
    opportunity_search_repository = (
        InMemoryOpportunitySearchRepository()
    )

    opportunity_search_service = OpportunitySearchService(
        opportunity_search_repository,
    )
    evidence_service = EvidenceService(
        evidence_repository,
        opportunity_search_repository,
    )

    opportunity_search = opportunity_search_service.create(
        OpportunitySearchCreate(
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
        )
    )

    request = EvidenceCreate(
        source_type="customer_review",
        source_name="Amazon review",
        content=(
            "The moisturizer works well, but the packaging "
            "creates too much waste."
        ),
        source_url="https://example.com/reviews/123",
    )

    result = evidence_service.create(
        opportunity_search.id, 
        request,
    )

    stored_evidence = evidence_repository.get_by_id(result.id)

    assert isinstance(result.id, UUID)
    assert stored_evidence == result
    assert result.opportunity_search_id == opportunity_search.id
    assert result.source_type == request.source_type
    assert result.source_name == request.source_name
    assert result.content == request.content
    assert result.source_url == request.source_url
    assert result.created_at.tzinfo is not None


def test_create_evidence_for_missing_opportunity_search() -> None:
    evidence_repository = InMemoryEvidenceRepository()
    opportunity_search_repository = (
        InMemoryOpportunitySearchRepository()
    )
    evidence_service = EvidenceService(
        evidence_repository,
        opportunity_search_repository,
    )

    missing_search_id = uuid4()
    request = EvidenceCreate(
        source_type="customer_review",
        source_name="Amazon review",
        content=(
            "The moisturizer works well, but the packaging "
            "creates too much waste."
        ),
        source_url="https://example.com/reviews/123",
    )

    with pytest.raises(
        OpportunitySearchNotFoundError,
        match=str(missing_search_id),
    ):
        evidence_service.create(missing_search_id, request)