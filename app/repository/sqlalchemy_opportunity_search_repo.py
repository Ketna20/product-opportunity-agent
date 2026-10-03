from uuid import UUID

from sqlalchemy.orm import Session

from app.model.opportunity_search_model import OpportunitySearchModel
from app.schema.opportunity_search import OpportunitySearchResponse


class SqlAlchemyOpportunitySearchRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(
        self,
        search: OpportunitySearchResponse,
    ) -> OpportunitySearchResponse:
        model = OpportunitySearchModel(
            id=search.id,
            product_category=search.product_category,
            market=search.market,
            target_customer=search.target_customer,
            objective=search.objective,
            constraints=search.constraints,
            initial_hypothesis=search.initial_hypothesis,
            status=search.status,
            created_at=search.created_at,
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
        search_id: UUID,
    ) -> OpportunitySearchResponse | None:
        model = self._session.get(
            OpportunitySearchModel,
            search_id,
        )

        if model is None:
            return None

        return self._to_response(model)

    @staticmethod
    def _to_response(
        model: OpportunitySearchModel,
    ) -> OpportunitySearchResponse:
        return OpportunitySearchResponse(
            id=model.id,
            product_category=model.product_category,
            market=model.market,
            target_customer=model.target_customer,
            objective=model.objective,
            constraints=model.constraints,
            initial_hypothesis=model.initial_hypothesis,
            status=model.status,
            created_at=model.created_at,
        )