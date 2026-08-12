from datetime import date
from typing import Annotated

from pydantic import Field

from willimakeit.services.airport_transfer_service import (
    AirportTransferRuleNotFoundError,
)
from willimakeit.services.flight_connection_service import (
    FlightConnectionError,
    FlightConnectionService,
)


class FlightConnectionTool:
    def __init__(
        self,
        service: FlightConnectionService,
    ) -> None:
        self._service = service

    async def assess_flight_connection(
        self,
        inbound_flight_number: Annotated[
            str,
            Field(description="Inbound commercial flight number, for example KM478."),
        ],
        outbound_flight_number: Annotated[
            str,
            Field(description="Outbound commercial flight number, for example DL221."),
        ],
        flight_date: Annotated[
            str,
            Field(description="Flight operating date in YYYY-MM-DD format."),
        ],
    ) -> dict[str, object]:
        """Assess whether two flights can be connected.

        The agent must provide only the inbound flight number,
        outbound flight number, and flight date. Flight times, terminals,
        transfer requirements, and risk are loaded and calculated by services.
        """

        print(
            "FLIGHT CONNECTION TOOL CALLED:",
            f"{inbound_flight_number=}",
            f"{outbound_flight_number=}",
            f"{flight_date=}",
            flush=True,
        )

        try:
            parsed_date = date.fromisoformat(flight_date)
            result = await self._service.assess(
                inbound_flight_number=inbound_flight_number,
                outbound_flight_number=outbound_flight_number,
                flight_date=parsed_date,
            )
        except ValueError as exc:
            return {
                "assessed": False,
                "error": "invalid_flight_date",
                "message": str(exc),
            }
        except FlightConnectionError as exc:
            return {
                "assessed": False,
                "error": "flight_connection_unavailable",
                "message": str(exc),
            }
        except AirportTransferRuleNotFoundError as exc:
            return {
                "assessed": False,
                "error": "airport_transfer_rule_not_found",
                "message": str(exc),
            }

        tool_result = {
            "assessed": True,
            **result.model_dump(mode="json"),
        }

        print(
            "FLIGHT CONNECTION TOOL RESULT:",
            tool_result,
            flush=True,
        )

        return tool_result
