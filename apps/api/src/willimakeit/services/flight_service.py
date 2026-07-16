from datetime import date

from willimakeit.providers.base import FlightProvider
from willimakeit.schemas.flight import FlightSchedule


class FlightService:
    def __init__(self, provider: FlightProvider) -> None:
        self._provider = provider

    async def find_flight(
        self, flight_number: str, flight_date: date
    ) -> FlightSchedule | None:
        return await self._provider.find_flight(flight_number, flight_date)
