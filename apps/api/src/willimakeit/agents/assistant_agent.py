from collections.abc import Awaitable, Callable
from datetime import date
from typing import Any

from willimakeit.schemas.assistant import AssistantResponse

FindFlightTool = Callable[[str, date], Awaitable[dict]]


async def run_assistant(
    message: str,
    agent: Any,
) -> AssistantResponse:
    result = await agent.run(message)

    return AssistantResponse(
        status="completed",
        message=result.text,
    )
