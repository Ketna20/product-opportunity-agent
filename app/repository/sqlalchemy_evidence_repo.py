from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.model.evidence_model import EvidenceModel
from app.model.evidence_chunk_model import EvidenceChunkModel

from app.schema.evidence import EvidenceResponse
from app.schema.evidence_chunk import EvidenceChunkResponse


class SqlAlchemyEvidenceRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(
        self,
        evidence: EvidenceResponse,
) -> EvidenceResponse:
        model = EvidenceModel(
            id=evidence.id,
            opportunity_search_id=evidence.opportunity_search_id,
            source_type=evidence.source_type,
            source_name=evidence.source_name,
            content=evidence.content,
            source_url=evidence.source_url,
            created_at=evidence.created_at,
        )

        self._session.add(model)

        try:
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise

        self._session.refresh(model)

        return self._to_response(model)

    def get_by_id(
        self,
        evidence_id: UUID,
    ) -> EvidenceResponse | None:
        model = self._session.get(
            EvidenceModel,
            evidence_id,
        )
        if model is None:
            return None
        return self._to_response(model)


    def find_by_opportunity_search_id(
        self,
        opportunity_search_id: UUID,
    ) -> list[EvidenceResponse]:
        stmt = (
            select(EvidenceModel)
            .where(
                EvidenceModel.opportunity_search_id == opportunity_search_id
            )
            .order_by(
                EvidenceModel.created_at,
                EvidenceModel.id,
            )
        )
        models = self._session.scalars(stmt).all()
        return [
            self._to_response(model)
            for model in models
        ]


    @staticmethod
    def _to_response(
        model: EvidenceModel,
    ) -> EvidenceResponse:
        return EvidenceResponse(
            id=model.id,
            opportunity_search_id=model.opportunity_search_id,
            source_type=model.source_type,
            source_name=model.source_name,
            content=model.content,
            source_url=model.source_url,
            created_at=model.created_at,
        )


    @staticmethod
    def _to_chunk_response(
        model: EvidenceChunkModel,
    ) -> EvidenceChunkResponse:
        return EvidenceChunkResponse(
            id=model.id,
            evidence_id=model.evidence_id,
            chunk_index=model.chunk_index,
            content=model.content,
            created_at=model.created_at,
        )

    def save_with_chunks(
        self,
        evidence: EvidenceResponse,
        chunks: list[EvidenceChunkResponse],
    ) -> EvidenceResponse:
        evidence_model = EvidenceModel(
            id=evidence.id,
            opportunity_search_id=evidence.opportunity_search_id,
            source_type=evidence.source_type,
            source_name=evidence.source_name,
            content=evidence.content,
            source_url=evidence.source_url,
            created_at=evidence.created_at,
        )

        try:
            self._session.add(evidence_model)
            self._session.flush()

            for chunk in chunks:
                chunk_model = EvidenceChunkModel(
                    id=chunk.id,
                    evidence_id=chunk.evidence_id,
                    chunk_index=chunk.chunk_index,
                    content=chunk.content,
                    created_at=chunk.created_at,
                )
                self._session.add(chunk_model)

            self._session.commit()
        except Exception:
            self._session.rollback()
            raise

        self._session.refresh(evidence_model)

        return self._to_response(evidence_model)


    def find_chunks_by_evidence_id(
        self,
        evidence_id: UUID,
    ) -> list[EvidenceChunkResponse]:
        stmt = (
            select(EvidenceChunkModel)
            .where(
                EvidenceChunkModel.evidence_id == evidence_id
            )
            .order_by(
                EvidenceChunkModel.chunk_index,
            )
        )
        models = self._session.scalars(stmt).all()

        return [
            self._to_chunk_response(model)
            for model in models
        ]