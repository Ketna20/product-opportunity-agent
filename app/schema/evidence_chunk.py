from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class EvidenceChunkResponse(BaseModel):
    id: UUID
    evidence_id: UUID
    chunk_index: int = Field(ge=0)
    content: str = Field(min_length=1)
    created_at: datetime