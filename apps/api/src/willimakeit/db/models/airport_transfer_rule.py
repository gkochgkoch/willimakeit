from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from willimakeit.db.base import Base


class AirportTransferRule(Base):
    __tablename__ = "airport_transfer_rules"
    __table_args__ = (
        UniqueConstraint(
            "airport_code",
            "arrival_terminal",
            "departure_terminal",
            "self_transfer",
            name="uq_airport_transfer_rule",
        ),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    airport_code: Mapped[str] = mapped_column(String(3), index=True)
    arrival_terminal: Mapped[str | None] = mapped_column(String(10))
    departure_terminal: Mapped[str | None] = mapped_column(String(10))

    terminal_transfer_minutes: Mapped[int] = mapped_column(Integer, default=0)
    security_minutes: Mapped[int] = mapped_column(Integer, default=0)
    immigration_minutes: Mapped[int] = mapped_column(Integer, default=0)
    baggage_recheck_minutes: Mapped[int] = mapped_column(Integer, default=0)

    self_transfer: Mapped[bool] = mapped_column(Boolean, default=False)

    source_type: Mapped[str] = mapped_column(String(50))
    source_url: Mapped[str | None] = mapped_column(Text)
    confidence: Mapped[str] = mapped_column(String(20), default="estimated")
    last_reviewed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
