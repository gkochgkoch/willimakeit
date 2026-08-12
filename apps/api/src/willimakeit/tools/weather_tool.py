from datetime import date
from typing import Annotated

from pydantic import Field

from willimakeit.schemas.weather import WeatherProviderError
from willimakeit.services.airport_location_service import AirportLocationService
from willimakeit.services.weather_service import WeatherService


class WeatherTool:
    def __init__(
        self,
        weather_service: WeatherService,
        airport__location_service: AirportLocationService,
    ) -> None:
        self.weather_service = weather_service
        self._airport_location_service = airport__location_service

    async def forecast(
        self,
        airport_code: Annotated[
            str, Field(description="Airport iata code, for example LHR")
        ],
        flight_date: Annotated[str, Field(description="Date of connection")],
    ) -> dict[str, object]:
        """Get the weather forecast for a specific airport code.
        Use this tool when weather information is requested.
        Returns hourly weather conditions for the requested date.
        """

        print(
            f"WEATHER TOOL CALLED: {airport_code=} {flight_date=}",
            flush=True,
        )

        location = await self._airport_location_service.coords(airport_code)
        if location is None:
            return {
                "assessed": False,
                "error": f"Airport {airport_code} not found",
            }

        parsed_date = date.fromisoformat(flight_date)

        try:
            forecast = await self.weather_service.forecast(
                latitude=location.latitude,
                longitude=location.longitude,
                start_date=parsed_date,
                end_date=parsed_date,
            )
        except WeatherProviderError as exc:
            return {
                "assessed": False,
                "message": str(exc),
            }

        tool_result = {
            "assessed": True,
            **forecast.model_dump(mode="json"),
        }

        return tool_result
