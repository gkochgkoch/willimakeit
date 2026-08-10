from uuid import UUID, uuid4

from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column

from willimakeit.db.base import Base


class Airport(Base):
    __tablename__ = "airports"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    airport_code: Mapped[str] = mapped_column(String(3), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(50), default="")
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
