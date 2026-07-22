from datetime import datetime

from willimakeit.schemas.connection import ConnectionAssessmentRequest
from willimakeit.services.connection_service import ConnectionService


class ConnectionTool:
    def __init__(
        self,
        connection_service: ConnectionService,
    ) -> None:
        self._connection_service = connection_service

    async def assess_connection(
        self,
        inbound_arrival: datetime,
        outbound_departure: datetime,
        minimum_connection_minutes: int,
        terminal_transfer_minutes: int = 0,
        security_check_minutes: int = 0,
        immigration_control_minutes: int = 0,
        disruption_buffer_minutes: int = 0,
    ) -> dict:
        """Calculate connection feasibility and risk.

        Use this tool for all connection-time calculations and risk
        classifications. Do not calculate connection risk manually.

        Args:
            inbound_arrival:
                Scheduled or estimated arrival time of the inbound flight.
            outbound_departure:
                Scheduled departure time of the onward flight.
            minimum_connection_minutes:
                Base minimum time required for the connection.
            terminal_transfer_minutes:
                Additional time needed to move between terminals.
            security_check_minutes:
                Additional time needed to pass security.
            immigration_control_minutes:
                Additional time needed for immigration or passport control.
            disruption_buffer_minutes:
                Additional time reserved for known disruption risk.
        """
        request = ConnectionAssessmentRequest(
            inbound_arrival=inbound_arrival,
            outbound_departure=outbound_departure,
            minimum_connection_minutes=minimum_connection_minutes,
            terminal_transfer_minutes=terminal_transfer_minutes,
            security_check_minutes=security_check_minutes,
            immigration_control_minutes=immigration_control_minutes,
            disruption_buffer_minutes=disruption_buffer_minutes,
        )

        result = self._connection_service.assess(request)
        return result.model_dump(mode="json")
