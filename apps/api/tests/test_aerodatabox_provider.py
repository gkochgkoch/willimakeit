import json
from datetime import date
from pathlib import Path

import httpx
import pytest

from willimakeit.providers.aerodatabox import AeroDataBoxFlightProvider

FIXTURES = Path(__file__).parent / "fixtures" / "aerodatabox"


@pytest.mark.asyncio
async def test_aerodatabox_provider() -> None:
    payload = json.loads((FIXTURES / "scheduled.json").read_text(encoding="utf-8"))

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == "/flights/number/QR4818/2026-07-15"
        assert request.headers["X-RapidAPI-Key"] == "testttt"
        assert request.headers["X-RapidAPI-Host"] == ("aerodatabox.p.rapidapi.com")

        return httpx.Response(
            status_code=200,
            json=payload,
        )

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as client:
        provider = AeroDataBoxFlightProvider(
            api_key="testttt",
            client=client,
            base_url="https://aerodatabox.p.rapidapi.com",
        )

        result = await provider.find_flight(
            flight_number="QR 4818", flight_date=date(2026, 7, 15)
        )

        assert result is not None
        assert result.flight_number == "QR 4818"
        assert result.flight_date == date(2026, 7, 15)
        assert result.departure_airport.iata == "MLA"
        assert result.arrival_airport.name == "Paris Charles de Gaulle"
        assert result.airline_iata == "QR"


@pytest.mark.asyncio
async def test_aerodatabox_provider_returns_none_for_empty_payload() -> None:
    payload = json.loads("[]")

    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(status_code=200, json=payload)

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as client:
        provider = AeroDataBoxFlightProvider(
            api_key="testttt",
            client=client,
            base_url="https://aerodatabox.p.rapidapi.com",
        )

        result = await provider.find_flight(
            flight_number="QR 4818", flight_date=date(2026, 7, 15)
        )

    assert result is None


@pytest.mark.asyncio
async def test_aerodatabox_provider_returns_none_204() -> None:

    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(status_code=204)

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as client:
        provider = AeroDataBoxFlightProvider(
            api_key="testttt",
            client=client,
            base_url="https://aerodatabox.p.rapidapi.com",
        )

        result = await provider.find_flight(
            flight_number="QR 4818", flight_date=date(2026, 7, 15)
        )

    assert result is None


@pytest.mark.asyncio
async def test_aerodatabox_provided_returns_none_404() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(status_code=404)

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as client:
        provider = AeroDataBoxFlightProvider(
            api_key="testttt",
            client=client,
            base_url="https://aerodatabox.p.rapidapi.com",
        )

        result = await provider.find_flight(
            flight_number="QR 4818", flight_date=date(2026, 7, 15)
        )

    assert result is None


@pytest.mark.asyncio
async def test_aerodatabox_provider_returns_503() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(status_code=503)

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as client:
        provider = AeroDataBoxFlightProvider(
            api_key="testttt",
            client=client,
            base_url="https://aerodatabox.p.rapidapi.com",
        )

        with pytest.raises(httpx.HTTPStatusError):
            await provider.find_flight(
                flight_number="QR 4818", flight_date=date(2026, 7, 15)
            )


@pytest.mark.asyncio
async def test_aerodatabox_handles_incomplete_response() -> None:
    payload = json.loads((FIXTURES / "incomplete.json").read_text(encoding="utf-8"))

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status_code=200, json=payload)

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as client:
        provider = AeroDataBoxFlightProvider(
            api_key="testtt",
            client=client,
            base_url="https://aerodatabox.p.rapidapi.com",
        )

        result = await provider.find_flight(
            flight_number="QR 4818", flight_date=date(2026, 7, 15)
        )
        assert result is not None
        assert result.arrival_airport.name == "Paris Charles de Gaulle"
        assert result.arrival_airport.iata is None
        assert result.scheduled_arrival_utc is None
        assert result.revised_arrival_utc is None
