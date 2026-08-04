from datetime import UTC, date, datetime

from willimakeit.schemas.airport_transfer import AirportTransferEstimate
from willimakeit.schemas.flight import Airport, FlightSchedule
from willimakeit.services.connection_service import ConnectionService
from willimakeit.services.flight_connection_service import FlightConnectionService
from willimakeit.tools.flight_connection_tool import FlightConnectionTool


class FakeFlightService:
    async def find_flight(
        self,
        flight_number: str,
        flight_date: date,
    ) -> FlightSchedule | None:
        flights = {
            "KM478": FlightSchedule(
                flight_number="KM478",
                flight_date=date(2026, 8, 1),
                departure_airport=Airport(iata="MLA"),
                arrival_airport=Airport(iata="CDG", terminal="2B"),
                scheduled_arrival_utc=datetime(2026, 8, 1, 7, 0, tzinfo=UTC),
            ),
            "DL221": FlightSchedule(
                flight_number="DL221",
                flight_date=date(2026, 8, 1),
                departure_airport=Airport(iata="CDG", terminal="2E"),
                arrival_airport=Airport(iata="SLC"),
                scheduled_departure_utc=datetime(2026, 8, 1, 9, 0, tzinfo=UTC),
            ),
        }
        flight = flights.get(flight_number)
        if flight is None or flight.flight_date != flight_date:
            return None
        return flight


class FakeAirportTransferService:
    async def estimate_transfer(
        self,
        airport_code: str,
        arrival_terminal: str,
        departure_terminal: str,
        self_transfer: bool,
    ) -> AirportTransferEstimate:
        assert airport_code == "CDG"
        assert arrival_terminal == "2B"
        assert departure_terminal == "2E"
        assert self_transfer is False

        return AirportTransferEstimate(
            airport_code="CDG",
            arrival_terminal="2B",
            departure_terminal="2E",
            terminal_transfer_minutes=30,
            security_minutes=20,
            immigration_minutes=10,
            baggage_recheck_minutes=0,
            total_required_minutes=60,
            self_transfer=False,
            confidence="test",
        )


async def test_assess_flight_connection_km478_to_dl221() -> None:
    service = FlightConnectionService(
        flight_service=FakeFlightService(),
        airport_transfer_service=FakeAirportTransferService(),
        connection_service=ConnectionService(),
    )
    tool = FlightConnectionTool(service=service)

    result = await tool.assess_flight_connection(
        inbound_flight_number="KM478",
        outbound_flight_number="DL221",
        flight_date="2026-08-01",
    )

    assert result["assessed"] is True
    assert result["available_minutes"] == 120
    assert result["required_minutes"] == 60
    assert result["margin_minutes"] == 60
    assert result["risk"] == "low"
