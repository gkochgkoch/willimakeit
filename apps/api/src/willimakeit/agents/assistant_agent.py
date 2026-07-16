from datetime import date

from willimakeit.schemas.assistant import AssistantResponse
from willimakeit.services.flight_service import FlightService


async def run_assistant(
    message: str,
    flight_service: FlightService,
) -> AssistantResponse:
    async def find_flight(
        flight_number: str,
        flight_date: date,
    ):
        return await flight_service.find_flight(
            flight_number=flight_number,
            flight_date=flight_date,
        )

    result = await find_flight(
        flight_number="QR4818",
        flight_date=date(2026, 7, 15),
    )

    if result is None:
        return AssistantResponse(
            status="accepted",
            message="Flight not found",
        )

    return AssistantResponse(
        status="accepted",
        message=f"Received: {message}. Result contains {result.flight_number}",
    )
