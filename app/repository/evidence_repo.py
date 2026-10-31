from typing import Protocol
from uuid import UUID

from app.schema.evidence import EvidenceResponse
from app.schema.evidence_chunk import EvidenceChunkResponse


class EvidenceRepository(Protocol):
    def save(
        self,
        evidence: EvidenceResponse,
    ) -> EvidenceResponse:
        ...

    def find_by_opportunity_search_id(
        self,
        opportunity_search_id: UUID,
    ) -> list[EvidenceResponse]:
        ...

    def save_with_chunks(
        self,
        evidence: EvidenceResponse,
        chunks: list[EvidenceChunkResponse],
    ) -> EvidenceResponse:
        ...

    def find_chunks_by_evidence_id(
        self,
        evidence_id: UUID,
    ) -> list[EvidenceChunkResponse]:
        ...


class InMemoryEvidenceRepository:
    def __init__(self) -> None:
        self._evidence: dict[UUID, EvidenceResponse] = {}
        self._chunks: dict[UUID, EvidenceChunkResponse] = {}

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
    
    def find_by_opportunity_search_id(
            self,
            opportunity_search_id: UUID,
        ) -> list[EvidenceResponse]:
        return [
            evidence
            for evidence in self._evidence.values()
            if evidence.opportunity_search_id == opportunity_search_id
        ]

    def save_with_chunks(
        self,
        evidence: EvidenceResponse,
        chunks: list[EvidenceChunkResponse],
    ) -> EvidenceResponse:
        self._evidence[evidence.id] = evidence

        for chunk in chunks:
            self._chunks[chunk.id] = chunk

        return evidence

    def find_chunks_by_evidence_id(
        self,
        evidence_id: UUID,
    ) -> list[EvidenceChunkResponse]:
        return sorted(
            (
                chunk
                for chunk in self._chunks.values()
                if chunk.evidence_id == evidence_id
            ),
            key=lambda c: c.chunk_index,
        )