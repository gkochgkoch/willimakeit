import asyncio
from datetime import date

import httpx

from willimakeit.providers.aerodatabox_mapper import map_flight_schedule
from willimakeit.schemas.flight import FlightSchedule


class AeroDataBoxFlightProvider:
    def __init__(
        self,
        *,
        api_key: str,
        client: httpx.AsyncClient,
        base_url: str,
    ) -> None:
        self._api_key = api_key
        self._client = client
        self._base_url = base_url.rstrip("/")
        self._rate_limit_lock = asyncio.Lock()
        self._last_request_at = 0.0

    async def find_flight(
        self,
        flight_number: str,
        flight_date: date,
    ) -> FlightSchedule | None:
        normalized_flight_number = flight_number.replace(" ", "").upper()

        async with self._rate_limit_lock:
            elapsed = asyncio.get_running_loop().time() - self._last_request_at

            if elapsed < 2:
                await asyncio.sleep(2 - elapsed)

            self._last_request_at = asyncio.get_running_loop().time()

            res = await self._client.get(
                (
                    f"{self._base_url}/flights/number/"
                    f"{normalized_flight_number}/{flight_date.isoformat()}"
                ),
                headers={
                    "X-RapidAPI-Key": self._api_key,
                    "X-RapidAPI-Host": "aerodatabox.p.rapidapi.com",
                },
            )

        if res.status_code in {204, 404}:
            return None

        res.raise_for_status()

        payload = res.json()

        if not payload:
            return None

        return map_flight_schedule(
            payload[0],
            flight_date=flight_date,
        )
