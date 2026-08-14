from datetime import date
from uuid import UUID, uuid4

from pgvector.sqlalchemy import VECTOR
from sqlalchemy import Date, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from willimakeit.db.base import Base


class AirlineRuleChunkModel(Base):
    __tablename__ = "airline_rule_chunks"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    airline_code: Mapped[str] = mapped_column(String(10))
    content: Mapped[str] = mapped_column(Text)
    section: Mapped[str | None] = mapped_column(String(100), nullable=True)
    effective_date: Mapped[date] = mapped_column(Date)
    embedding: Mapped[list[float]] = mapped_column(VECTOR(1024))
