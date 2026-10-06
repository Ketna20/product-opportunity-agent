from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class EvidenceCreate(BaseModel):
    source_type: str = Field(
        min_length=2,
        max_length=50,
        description="Type of evidence such as customer review, support ticket.",
    )

    source_name: str = Field(
        min_length=2,
        max_length=200,
        description="Human-readable source such as Amazon review.",
    )

    content: str = Field(
        min_length=10,
        max_length=10000,
        description="The actual evidence text.",
    )

    source_url: str | None = Field(
        default=None,
        max_length=2000,
        description="Optional link back to the original source.",
    )


class EvidenceResponse(BaseModel):
    id: UUID
    opportunity_search_id: UUID
    source_type: str
    source_name: str
    content: str
    source_url: str | None
    created_at: datetime