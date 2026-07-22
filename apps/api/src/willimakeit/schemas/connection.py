from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class ConnectionRisk(StrEnum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    IMPOSSIBLE = "impossible"
    UNKNOWN = "unknown"


class ConnectionAssessmentRequest(BaseModel):
    inbound_arrival: datetime
    outbound_departure: datetime
    minimum_connection_minutes: int = Field(ge=0)
    terminal_transfer_minutes: int = Field(default=0, ge=0)
    security_check_minutes: int = Field(default=0, ge=0)
    immigration_control_minutes: int = Field(default=0, ge=0)
    disruption_buffer_minutes: int = Field(default=0, ge=0)


class ConnectionAssessment(BaseModel):
    available_minutes: int
    required_minutes: int
    margin_minutes: int
    risk: ConnectionRisk
    reasons: list[str]
