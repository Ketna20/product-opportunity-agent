from typing import Protocol
from uuid import UUID

from app.schema.evidence import EvidenceResponse


class EvidenceRepository(Protocol):
    def save(
        self,
        evidence: EvidenceResponse,
    )-> EvidenceResponse:
        ...



class InMemoryEvidenceRepository:
    def __init__(self) -> None:
        self._evidence: dict[UUID, EvidenceResponse] = {}

    def save(
        self,
        evidence: EvidenceResponse,
    ) -> EvidenceResponse:
        self._evidence[evidence.id] = evidence
        return evidence

    def get_by_id(
        self,
        evidence_id: UUID,
    ) -> EvidenceResponse | None:
        return self._evidence.get(evidence_id)
    
    