from datetime import datetime, UTC
from uuid import UUID, uuid4

from sqlalchemy import  DateTime, Enum, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.schema.opportunity_search import OpportunitySearchStatus

class OpportunitySearchModel(Base):
    __tablename__ = "opportunity_searches"

    id: Mapped[UUID] = mapped_column(
        primary_key=True, 
        default=uuid4
    )
    product_category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    market: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    target_customer: Mapped[str] = mapped_column(
        String(300),
        nullable=False,
    )
    objective: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )
    constraints: Mapped[list[str]] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
    )
    initial_hypothesis: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )
    status: Mapped[OpportunitySearchStatus] = mapped_column(
        Enum(
            OpportunitySearchStatus,
            name="opportunity_search_status",
            values_callable=lambda statuses: [
                status.value for status in statuses
            ],
        ),
        default=OpportunitySearchStatus.CREATED,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    