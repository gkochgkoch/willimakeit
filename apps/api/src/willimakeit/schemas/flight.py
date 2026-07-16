from datetime import date, datetime

from pydantic import BaseModel


class Airport(BaseModel):
    icao: str | None = None
    name: str | None = None
    iata: str | None = None
    time_zone: str | None = None
    terminal: str | None = None
    gate: str | None = None


class FlightSchedule(BaseModel):
    flight_number: str
    flight_date: date
    departure_airport: Airport
    arrival_airport: Airport
    scheduled_departure_utc: datetime | None = None
    scheduled_departure_local: datetime | None = None
    scheduled_arrival_utc: datetime | None = None
    scheduled_arrival_local: datetime | None = None
    revised_departure_utc: datetime | None = None
    revised_arrival_utc: datetime | None = None
    airline_name: str | None = None
    airline_iata: str | None = None
