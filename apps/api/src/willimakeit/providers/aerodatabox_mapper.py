from datetime import date
from typing import Any

from willimakeit.schemas.flight import Airport, FlightSchedule


def map_flight_schedule(raw: dict[str, Any], *, flight_date: date) -> FlightSchedule:

    departure = raw.get("departure") or {}
    arrival = raw.get("arrival") or {}
    departure_airport = departure.get("airport") or {}
    arrival_airport = arrival.get("airport") or {}
    departure_scheduled = departure.get("scheduledTime") or {}
    arrival_scheduled = arrival.get("scheduledTime") or {}
    departure_revised = departure.get("revisedTime") or {}
    arrival_revised = arrival.get("revisedTime") or {}
    airline = raw.get("airline") or {}

    return FlightSchedule(
        flight_number=raw["number"],
        flight_date=flight_date,
        departure_airport=Airport(
            icao=departure_airport.get("icao"),
            iata=departure_airport.get("iata"),
            name=departure_airport.get("name"),
            time_zone=departure_airport.get("timeZone"),
            terminal=departure.get("terminal"),
            gate=departure.get("gate"),
        ),
        arrival_airport=Airport(
            icao=arrival_airport.get("icao"),
            iata=arrival_airport.get("iata"),
            name=arrival_airport.get("name"),
            time_zone=arrival_airport.get("timeZone"),
            terminal=arrival.get("terminal"),
            gate=arrival.get("gate"),
        ),
        scheduled_departure_utc=departure_scheduled.get("utc"),
        scheduled_departure_local=departure_scheduled.get("local"),
        scheduled_arrival_utc=arrival_scheduled.get("utc"),
        scheduled_arrival_local=arrival_scheduled.get("local"),
        revised_departure_utc=departure_revised.get("utc"),
        revised_arrival_utc=arrival_revised.get("utc"),
        airline_name=airline.get("name"),
        airline_iata=airline.get("iata"),
    )
