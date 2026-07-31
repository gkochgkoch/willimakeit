from datetime import date
from typing import Annotated

from pydantic import Field

from willimakeit.services.flight_service import FlightService


def create_flight_tool(flight_service: FlightService):
    async def find_flight(
        flight_number: Annotated[
            str,
            Field(
                description=(
                    "Commercial flight number, for example KM478. "
                    "Use the airline designator and flight number."
                )
            ),
        ],
        flight_date: Annotated[
            str,
            Field(
                description=(
                    "Flight operating date in YYYY-MM-DD format, "
                    "for example 2026-08-01."
                )
            ),
        ],
    ) -> dict[str, object]:
        """Find a flight by commercial flight number and operating date.

        Returns the flight schedule and status when found.
        If the provider cannot retrieve the flight, returns found=false
        and an error describing the failure.

        Call this tool independently for each flight the user asks about.
        """

        print(
            "FLIGHT TOOL CALLED:",
            f"{flight_number=}",
            f"{flight_date=}",
            flush=True,
        )

        try:
            parsed_date = date.fromisoformat(flight_date)

            result = await flight_service.find_flight(
                flight_number=flight_number,
                flight_date=parsed_date,
            )

        except Exception as exc:
            print(
                "FLIGHT TOOL ERROR:",
                f"{flight_number=}",
                f"{flight_date=}",
                f"{type(exc).__name__}: {exc}",
                flush=True,
            )

            return {
                "found": False,
                "flight_number": flight_number,
                "flight_date": flight_date,
                "error": "flight_lookup_failed",
                "message": str(exc),
            }

        if result is None:
            print(
                "FLIGHT TOOL RESULT: NOT FOUND",
                f"{flight_number=}",
                f"{flight_date=}",
                flush=True,
            )

            return {
                "found": False,
                "flight_number": flight_number,
                "flight_date": flight_date,
                "error": "flight_not_found",
            }

        tool_result = {
            "found": True,
            "flight_number": flight_number,
            "flight_date": flight_date,
            "flight": result.model_dump(mode="json"),
        }

        print(
            "FLIGHT TOOL RESULT:",
            tool_result,
            flush=True,
        )

        return tool_result

    return find_flight
