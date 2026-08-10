from datetime import date
from typing import Protocol

from willimakeit.schemas.flight import FlightSchedule
from willimakeit.schemas.weather import Weather


class FlightNotFoundError(Exception):
    pass


class FlightProvider(Protocol):
    async def find_flight(
        self, flight_number: str, flight_date: date
    ) -> FlightSchedule | None: ...


class WeatherProvider(Protocol):
    async def forecast(
        self,
        latitude: float,
        longitude: float,
        start_date: date,
        end_date: date,
    ) -> Weather: ...
