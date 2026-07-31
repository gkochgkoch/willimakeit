import asyncio

from willimakeit.db.session import async_session_factory
from willimakeit.services.airport_transfer_service import AirportTransferService
from willimakeit.tools.airport_transfer_tool import AirportTransferTool


async def main() -> None:
    service = AirportTransferService(
        session_factory=async_session_factory,
    )

    tool = AirportTransferTool(
        service=service,
    )

    result = await tool.get_airport_transfer_estimate(
        airport_code="LHR",
        arrival_terminal="2",
        departure_terminal="5",
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(main())
