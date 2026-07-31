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
        inbound_arrival: str,
        outbound_departure: str,
        minimum_connection_minutes: int,
        terminal_transfer_minutes: int = 0,
        security_check_minutes: int = 0,
        immigration_control_minutes: int = 0,
        disruption_buffer_minutes: int = 0,
    ) -> dict:
        """Assess whether a flight connection is feasible.

        Use only when arrival and departure times are known and
        the user asks whether the connection can be made.

        Times must use ISO-8601 format.
        """

        print(
            "CONNECTION TOOL CALLED:",
            f"{inbound_arrival=}",
            f"{outbound_departure=}",
            f"{minimum_connection_minutes=}",
            f"{terminal_transfer_minutes=}",
            f"{security_check_minutes=}",
            f"{immigration_control_minutes=}",
            f"{disruption_buffer_minutes=}",
            flush=True,
        )

        inbound_dt = datetime.fromisoformat(inbound_arrival)
        outbound_dt = datetime.fromisoformat(outbound_departure)
        request = ConnectionAssessmentRequest(
            inbound_arrival=inbound_dt,
            outbound_departure=outbound_dt,
            minimum_connection_minutes=minimum_connection_minutes,
            terminal_transfer_minutes=terminal_transfer_minutes,
            security_check_minutes=security_check_minutes,
            immigration_control_minutes=immigration_control_minutes,
            disruption_buffer_minutes=disruption_buffer_minutes,
        )

        result = self._connection_service.assess(request)

        tool_result = result.model_dump(mode="json")

        print(
            "CONNECTION TOOL RESULT:",
            tool_result,
            flush=True,
        )

        return tool_result
