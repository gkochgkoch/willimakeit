from fastapi import APIRouter, Request

from willimakeit.agents.assistant_agent import run_assistant
from willimakeit.schemas.assistant import AssistantRequest, AssistantResponse

router = APIRouter()


@router.post(
    "/assistant/ask",
    response_model=AssistantResponse,
)
async def assistant_ask(
    body: AssistantRequest,
    request: Request,
) -> AssistantResponse:

    return await run_assistant(
        message=body.message,
        agent=request.app.state.assistant_agent,
    )
