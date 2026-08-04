from datetime import date

from willimakeit.schemas.connection import (
    ConnectionAssessment,
    ConnectionAssessmentRequest,
)
from willimakeit.services.airport_transfer_service import AirportTransferService
from willimakeit.services.connection_service import ConnectionService
from willimakeit.services.flight_service import FlightService


class FlightConnectionError(Exception):
    pass


class FlightConnectionService:
    def __init__(
        self,
        flight_service: FlightService,
        airport_transfer_service: AirportTransferService,
        connection_service: ConnectionService,
    ) -> None:
        self._flight_service = flight_service
        self._airport_transfer_service = airport_transfer_service
        self._connection_service = connection_service

    async def assess(
        self,
        inbound_flight_number: str,
        outbound_flight_number: str,
        flight_date: date,
    ) -> ConnectionAssessment:
        inbound = await self._flight_service.find_flight(
            inbound_flight_number,
            flight_date,
        )
        if inbound is None:
            raise FlightConnectionError("inbound flight is not found")

        outbound = await self._flight_service.find_flight(
            outbound_flight_number,
            flight_date,
        )
        if outbound is None:
            raise FlightConnectionError("outbound flight is not found")

        arrival_airport = self._airport_code(inbound.arrival_airport.iata)
        departure_airport = self._airport_code(outbound.departure_airport.iata)
        if arrival_airport is None or departure_airport is None:
            raise FlightConnectionError("connection airport is missing")

        if arrival_airport != departure_airport:
            raise FlightConnectionError(
                "inbound arrival airport does not match outbound departure airport"
            )

        if inbound.scheduled_arrival_utc is None:
            raise FlightConnectionError("inbound scheduled arrival time is missing")
        if outbound.scheduled_departure_utc is None:
            raise FlightConnectionError("outbound scheduled departure time is missing")

        arrival_terminal = inbound.arrival_airport.terminal
        departure_terminal = outbound.departure_airport.terminal
        if arrival_terminal is None:
            raise FlightConnectionError("inbound arrival terminal is missing")
        if departure_terminal is None:
            raise FlightConnectionError("outbound departure terminal is missing")

        transfer = await self._airport_transfer_service.estimate_transfer(
            airport_code=arrival_airport,
            arrival_terminal=arrival_terminal,
            departure_terminal=departure_terminal,
            self_transfer=False,
        )

        request = ConnectionAssessmentRequest(
            inbound_arrival=inbound.scheduled_arrival_utc,
            outbound_departure=outbound.scheduled_departure_utc,
            minimum_connection_minutes=transfer.baggage_recheck_minutes,
            terminal_transfer_minutes=transfer.terminal_transfer_minutes,
            security_check_minutes=transfer.security_minutes,
            immigration_control_minutes=transfer.immigration_minutes,
            disruption_buffer_minutes=0,
        )

        return self._connection_service.assess(request)

    @staticmethod
    def _airport_code(value: str | None) -> str | None:
        if value is None:
            return None
        return value.upper()
