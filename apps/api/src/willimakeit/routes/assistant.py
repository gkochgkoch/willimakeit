from fastapi import APIRouter, Request

from willimakeit.agents.assistant_agent import run_assistant
from willimakeit.schemas.assistant import AssistantRequest, AssistantResponse

router = APIRouter()


@router.post("/assistant/ask")
async def assistant_ask(body: AssistantRequest, request: Request) -> AssistantResponse:
    flight_service = request.app.state.flight_service

    return await run_assistant(
        message=body.message,
        flight_service=flight_service,
    )
