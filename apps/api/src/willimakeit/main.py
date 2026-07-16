from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from willimakeit.config import settings
from willimakeit.providers.aerodatabox import AeroDataBoxFlightProvider
from willimakeit.routes.assessments import router as assessment_router
from willimakeit.routes.assistant import router as assistant_router
from willimakeit.routes.health import router as health_router
from willimakeit.services.flight_service import FlightService


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with httpx.AsyncClient() as http_client:
        provider = AeroDataBoxFlightProvider(
            api_key=settings.rapidapi_key,
            client=http_client,
            base_url=settings.aerodatabox_base_url,
        )

        app.state.flight_service = FlightService(provider=provider)

        yield


app = FastAPI(title="Will I Make It API", version="0.1.0", lifespan=lifespan)

app.include_router(health_router)
app.include_router(assistant_router)
app.include_router(assessment_router)
