from fastapi import Request

from willimakeit.services.flight_service import FlightService
from willimakeit.services.weather_service import WeatherService


def get_flight_service(request: Request) -> FlightService:
    return request.app.state.flight_service


def get_weather_service(request: Request) -> WeatherService:
    return request.app.state.weather_service
