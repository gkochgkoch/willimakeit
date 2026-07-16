from fastapi import Request

from willimakeit.services.flight_service import FlightService


def get_flight_service(request: Request) -> FlightService:
    return request.app.state.flight_service
