from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from willimakeit.db.models.airports import Airport


class AirportRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_code(self, code: str) -> Airport | None:
        statement = select(Airport).where(Airport.airport_code == code.upper())
        return await self._session.scalar(statement)
