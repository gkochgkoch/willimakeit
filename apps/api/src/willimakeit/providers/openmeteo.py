from datetime import date

import httpx

from willimakeit.schemas.weather import (
    HourlyWeather,
    Weather,
    WeatherProvider503Error,
    WeatherProviderNoContentError,
    WeatherProviderTimeoutError,
)


class OpenMeteoWeatherProvider:
    def __init__(
        self,
        client: httpx.AsyncClient,
        base_url: str,
    ) -> None:
        self._client = client
        self._base_url = base_url

    async def forecast(
        self, latitude: float, longitude: float, start_date: date, end_date: date
    ) -> Weather:
        hourly = "visibility,snowfall,wind_speed_80m"
        params: dict[str, str | float] = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": hourly,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        }

        try:
            response = await self._client.get(self._base_url, params=params)
            response.raise_for_status()
        except httpx.TimeoutException as exc:
            raise WeatherProviderTimeoutError("custom timeout error") from exc
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 503:
                raise WeatherProvider503Error("test 500 error") from exc
            raise

        if response.status_code == 204:
            raise WeatherProviderNoContentError("Open Meteoo returned no content")

        result = response.json()
        mapped_result = []
        for time, visibility, snowfall, wind_speed_80m in zip(
            result["hourly"]["time"],
            result["hourly"]["visibility"],
            result["hourly"]["snowfall"],
            result["hourly"]["wind_speed_80m"],
            strict=True,
        ):
            mapped_result.append(
                HourlyWeather(
                    timestamp=time,
                    visibility=visibility,
                    snowfall=snowfall,
                    wind_speed_80m=wind_speed_80m,
                )
            )
        return Weather(hourly=mapped_result)
