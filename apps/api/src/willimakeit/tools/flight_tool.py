from datetime import date
from typing import Any

from willimakeit.services.flight_service import FlightService


def create_flight_tool(
    flight_service: FlightService,
) -> Any:
    async def find_flight(
        flight_number: str,
        flight_date: date,
    ) -> dict:
        """Find a flight by flight number and operating date.

        Args:
            flight_number:
                Commercial flight number, such as QR4818.
            flight_date:
                Local date on which the flight operates.
        """
        result = await flight_service.find_flight(
            flight_number=flight_number,
            flight_date=flight_date,
        )

        if result is None:
            return {
                "found": False,
                "flight_number": flight_number,
                "flight_date": flight_date.isoformat(),
            }

        return {
            "found": True,
            "flight": result.model_dump(mode="json"),
        }

    return find_flight
