from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from willimakeit.repositories.airport_repository import AirportRepository
from willimakeit.schemas.airport_location import AirportLocation


class AirportLocationService:
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self._session_factory = session_factory

    async def coords(self, code: str) -> AirportLocation | None:
        async with self._session_factory() as session:
            repository = AirportRepository(session)
            airport = await repository.find_by_code(code)
            if airport is None:
                return None
            return AirportLocation(
                airport_code=airport.airport_code,
                latitude=airport.latitude,
                longitude=airport.longitude,
            )
