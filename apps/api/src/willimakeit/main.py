from contextlib import asynccontextmanager

import httpx
from agent_framework.openai import OpenAIChatClient
from fastapi import FastAPI

from willimakeit.agents.prompts import CONNECTION_ASSISTANT_SYSTEM_PROMPT
from willimakeit.config import settings
from willimakeit.providers.aerodatabox import AeroDataBoxFlightProvider
from willimakeit.routes.assessments import router as assessment_router
from willimakeit.routes.assistant import router as assistant_router
from willimakeit.routes.health import router as health_router
from willimakeit.services.connection_service import ConnectionService
from willimakeit.services.flight_service import FlightService
from willimakeit.tools.connection_tool import ConnectionTool
from willimakeit.tools.flight_tool import create_flight_tool


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with httpx.AsyncClient() as http_client:
        flight_provider = AeroDataBoxFlightProvider(
            client=http_client,
            base_url=settings.aerodatabox_base_url,
            api_key=settings.rapidapi_key,
        )

        flight_service = FlightService(
            provider=flight_provider,
        )

        connection_service = ConnectionService()

        find_flight = create_flight_tool(
            flight_service=flight_service,
        )

        connection_tool = ConnectionTool(
            connection_service=connection_service,
        )

        assistant_agent = OpenAIChatClient(
            api_key="ollama",
            base_url=settings.ollama_base_url,
            model=settings.ollama_model,
        ).as_agent(
            name="ConnectionAssessmentAssistant",
            instructions=CONNECTION_ASSISTANT_SYSTEM_PROMPT,
            tools=[
                find_flight,
                connection_tool.assess_connection,
            ],
        )

        app.state.flight_service = flight_service
        app.state.connection_service = connection_service
        app.state.assistant_agent = assistant_agent

        yield


app = FastAPI(
    title="Will I Make It API",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(assistant_router)
app.include_router(assessment_router)
