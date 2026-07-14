from fastapi import FastAPI

from willimakeit.routes.assessments import router as assessment_router
from willimakeit.routes.assistant import router as assistant_router
from willimakeit.routes.health import router as health_router

app = FastAPI(
    title="Will I Make It API",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(assistant_router)
app.include_router(assessment_router)
