from datetime import date

from pydantic import BaseModel


class AirlineRuleChunk(BaseModel):
    airline_code: str
    content: str
    section: str | None = None
    effective_date: date


class EmbeddedAirlineRule:
    chunk: AirlineRuleChunk
    embedding: list[float]
