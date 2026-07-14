from uuid import uuid4

from fastapi import APIRouter

from willimakeit.schemas.assistant import AssistantRequest, AssistantResponse

router = APIRouter()


@router.post("/assistant/ask")
async def assistant_ask(request: AssistantRequest) -> AssistantResponse:
    return AssistantResponse(
        status="accepted", assessment_id=str(uuid4()), message=request.message
    )
