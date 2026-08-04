from typing import Annotated

from pydantic import Field

from willimakeit.services.airport_transfer_service import (
    AirportTransferRuleNotFoundError,
    AirportTransferService,
)


class AirportTransferTool:
    def __init__(
        self,
        service: AirportTransferService,
    ) -> None:
        self._service = service

    async def get_airport_transfer_estimate(
        self,
        airport_code: Annotated[
            str,
            Field(description="IATA airport code, for example LHR."),
        ],
        arrival_terminal: Annotated[
            str,
            Field(description="Arrival terminal, for example 2."),
        ],
        departure_terminal: Annotated[
            str,
            Field(description="Departure terminal, for example 5."),
        ],
    ) -> dict[str, object]:
        """Get airport transfer requirements between two terminals.

        Use this tool when the user asks about:
        - terminal transfer requirements
        - transfer time
        - security during a transfer
        - immigration during a transfer
        - baggage recheck requirements

        Do NOT use this tool to calculate whether the passenger
        will make the connection. Use assess_flight_connection for that.
        """

        print(
            "AIRPORT TOOL CALLED:",
            f"{airport_code=!r}",
            f"{arrival_terminal=!r}",
            f"{departure_terminal=!r}",
            flush=True,
        )
        try:
            estimate = await self._service.estimate_transfer(
                airport_code=airport_code,
                arrival_terminal=arrival_terminal,
                departure_terminal=departure_terminal,
                self_transfer=False,
            )
        except AirportTransferRuleNotFoundError as exc:
            return {
                "found": False,
                "error": str(exc),
            }

        return {
            "found": True,
            **estimate.model_dump(),
        }
