from datetime import date
from typing import Protocol

from willimakeit.schemas.flight import FlightSchedule


class FlightNotFoundError(Exception):
    pass


class FlightProvider(Protocol):
    async def find_flight(
        self, flight_number: str, flight_date: date
    ) -> FlightSchedule | None: ...
