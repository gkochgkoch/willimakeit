from datetime import date

from willimakeit.providers.base import WeatherProvider
from willimakeit.schemas.weather import Weather


class WeatherService:
    def __init__(self, provider: WeatherProvider) -> None:
        self._provider = provider

    async def forecast(
        self, latitude: float, longitude: float, start_date: date, end_date: date
    ) -> Weather:
        return await self._provider.forecast(
            latitude=latitude,
            longitude=longitude,
            start_date=start_date,
            end_date=end_date,
        )
