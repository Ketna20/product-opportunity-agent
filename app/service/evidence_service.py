from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.repository.evidence_repo import (
    EvidenceRepository,
)

from app.schema.evidence import (
    EvidenceCreate,
    EvidenceResponse,
)

from app.repository.opportunity_search_repo import (
    OpportunitySearchRepository,
)


class OpportunitySearchNotFoundError(Exception):
    pass



class EvidenceService:
    def __init__(
        self,
        evidence_repository: EvidenceRepository,
        opportunity_search_repository: OpportunitySearchRepository,
    ) -> None:
        self._evidence_repository = evidence_repository
        self._opportunity_search_repository = opportunity_search_repository

    def create(
        self,
        opportunity_search_id: UUID,
        request: EvidenceCreate,
) -> EvidenceResponse:
        opportunity_search = self._opportunity_search_repository.get_by_id(
            opportunity_search_id,
        )
        if opportunity_search is None:
            raise OpportunitySearchNotFoundError(
                f"Opportunity search {opportunity_search_id} not found"
            )
        evidence = EvidenceResponse(
            id=uuid4(),
            opportunity_search_id=opportunity_search_id,
            source_type=request.source_type,
            source_name=request.source_name,
            content=request.content,
            source_url=request.source_url,
            created_at=datetime.now(UTC),
        )
        return self._evidence_repository.save(evidence)
