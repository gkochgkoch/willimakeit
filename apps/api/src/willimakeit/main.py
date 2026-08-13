from contextlib import asynccontextmanager

import httpx
from agent_framework.openai import OpenAIChatClient
from fastapi import FastAPI

from willimakeit.agents.prompts import CONNECTION_ASSISTANT_SYSTEM_PROMPT
from willimakeit.config import settings
from willimakeit.db.session import async_session_factory
from willimakeit.middleware.request_id import (
    register_request_id_middleware,
)
from willimakeit.providers.aerodatabox import AeroDataBoxFlightProvider
from willimakeit.providers.openmeteo import OpenMeteoWeatherProvider
from willimakeit.routes.assessments import router as assessment_router
from willimakeit.routes.assistant import router as assistant_router
from willimakeit.routes.health import router as health_router
from willimakeit.routes.weather import router as weather_router
from willimakeit.services.airport_location_service import AirportLocationService
from willimakeit.services.airport_transfer_service import AirportTransferService
from willimakeit.services.connection_service import ConnectionService
from willimakeit.services.flight_connection_service import FlightConnectionService
from willimakeit.services.flight_service import FlightService
from willimakeit.services.weather_service import WeatherService
from willimakeit.tools.airport_transfer_tool import AirportTransferTool
from willimakeit.tools.flight_connection_tool import FlightConnectionTool
from willimakeit.tools.flight_tool import create_flight_tool
from willimakeit.tools.weather_tool import WeatherTool


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with httpx.AsyncClient(timeout=settings.timeout) as http_client:
        weather_provider = OpenMeteoWeatherProvider(
            client=http_client, base_url=settings.openmeteo_base_url
        )

        weather_service = WeatherService(provider=weather_provider)
        airport_location_service = AirportLocationService(
            session_factory=async_session_factory,
        )

        flight_provider = AeroDataBoxFlightProvider(
            client=http_client,
            base_url=settings.aerodatabox_base_url,
            api_key=settings.rapidapi_key,
        )

        flight_service = FlightService(
            provider=flight_provider,
        )

        airport_transfer_service = AirportTransferService(
            session_factory=async_session_factory
        )

        connection_service = ConnectionService()

        find_flight = create_flight_tool(
            flight_service=flight_service,
        )

        flight_connection_service = FlightConnectionService(
            flight_service=flight_service,
            airport_transfer_service=airport_transfer_service,
            connection_service=connection_service,
            airport_location_service=airport_location_service,
            weather_service=weather_service,
        )

        airport_transfer_tool = AirportTransferTool(service=airport_transfer_service)
        flight_connection_tool = FlightConnectionTool(service=flight_connection_service)
        weather_tool = WeatherTool(
            weather_service=weather_service,
            airport__location_service=airport_location_service,
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
                airport_transfer_tool.get_airport_transfer_estimate,
                flight_connection_tool.assess_flight_connection,
                weather_tool.forecast,
            ],
        )

        app.state.flight_service = flight_service
        app.state.connection_service = connection_service
        app.state.flight_connection_service = flight_connection_service
        app.state.assistant_agent = assistant_agent
        app.state.weather_service = weather_service

        yield


app = FastAPI(
    title="Will I Make It API",
    version="0.1.0",
    lifespan=lifespan,
)

register_request_id_middleware(app)

app.include_router(health_router)
app.include_router(assistant_router)
app.include_router(assessment_router)
app.include_router(weather_router)
