from datetime import date

from fastapi import APIRouter, Depends

from willimakeit.dependencies import get_weather_service
from willimakeit.schemas.weather import Weather
from willimakeit.services.weather_service import WeatherService

router = APIRouter()


@router.get("/weather")
async def weather(
    latitude: float = 51.4704,
    longitude: float = -0.4586,
    start_date: date = date(2026, 8, 12),
    end_date: date = date(2026, 8, 12),
    service: WeatherService = Depends(get_weather_service),  # noqa: B008
) -> Weather:

    return await service.forecast(
        latitude=latitude, longitude=longitude, start_date=start_date, end_date=end_date
    )
