from datetime import datetime, UTC
from uuid import UUID, uuid4

from sqlalchemy import (
    DateTime, 
    ForeignKey,
    Integer, 
    Text, 
    UniqueConstraint, 
    CheckConstraint
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class EvidenceChunkModel(Base):
    __tablename__ = "evidence_chunks"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    evidence_id: Mapped[UUID] = mapped_column(
        ForeignKey("evidence_items.id"),
        nullable=False,
    )

    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "evidence_id",
            "chunk_index",
            name="uq_evidence_chunks_evidence_id_chunk_index",
        ),
        CheckConstraint(
            "chunk_index >= 0",
            name="ck_evidence_chunks_chunk_index_nonnegative",
        ),
    )