from collections.abc import Awaitable, Callable
from datetime import date

from willimakeit.schemas.assistant import AssistantResponse

FindFlightTool = Callable[[str, date], Awaitable[dict]]


async def run_assistant(
    message: str,
    find_flight: FindFlightTool,
) -> AssistantResponse:
    result = await find_flight(
        "QR4818",
        date(2026, 7, 15),
    )

    if not result["found"]:
        return AssistantResponse(
            status="completed",
            message="Flight not found.",
        )

    flight = result["flight"]

    return AssistantResponse(
        status="completed",
        message=(f"Received: {message}. Found flight {flight['flight_number']}."),
    )
