from uuid import UUID

from app.schema.opportunity_search import OpportunitySearchResponse


class InMemoryOpportunitySearchRepository:
    def __init__(self) -> None:
        self._searches: dict[UUID, OpportunitySearchResponse] = {}

    def save(
        self,
        search: OpportunitySearchResponse,
    ) -> OpportunitySearchResponse:
        self._searches[search.id] = search
        return search

    def get_by_id(
        self,
        search_id: UUID,
    ) -> OpportunitySearchResponse | None:
        return self._searches.get(search_id)