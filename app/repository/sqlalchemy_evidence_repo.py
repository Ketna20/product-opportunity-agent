from uuid import UUID

from sqlalchemy.orm import Session

from app.model.evidence_model import EvidenceModel

from app.schema.evidence import EvidenceResponse


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
    