from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get("/assessments")
async def assessments() -> dict[str, list[Any]]:
    return {"assessments": []}


@router.get("/assessments/{assessment_id}")
async def get_assessment(assessment_id: str) -> dict[str, str]:
    return {"status": "accepted", "assessment_id": assessment_id}
