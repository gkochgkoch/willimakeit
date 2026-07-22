from typing import Literal

from pydantic import BaseModel, Field


class AssistantRequest(BaseModel):
    message: str = Field(min_length=1)


class AssistantResponse(BaseModel):
    status: Literal["completed", "need_more_information"]
    assessment_id: str | None = None
    message: str | None = None
