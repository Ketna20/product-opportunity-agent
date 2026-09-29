from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field


class OpportunitySearchStatus(StrEnum):
    CREATED = "created"


class OpportunitySearchCreate(BaseModel):
    product_category: str = Field(
        min_length=2,
        max_length=100,
        description="The product category being investigated",
    )
    market: str = Field(
        min_length=2,
        max_length=100,
        description="The geographic market being investigated",
    )
    target_customer: str = Field(
        min_length=5,
        max_length=300,
        description="The customer segment the opportunity should serve",
    )
    objective: str = Field(
        min_length=10,
        max_length=1000,
        description="The product opportunity search objective",
    )
    constraints: list[str] = Field(default_factory=list)
    initial_hypothesis: str | None = Field(
        default=None,
        max_length=1000,
    )


class OpportunitySearchResponse(BaseModel):
    id: UUID
    product_category: str
    market: str
    target_customer: str
    objective: str
    constraints: list[str]
    initial_hypothesis: str | None
    status: OpportunitySearchStatus
    created_at: datetime