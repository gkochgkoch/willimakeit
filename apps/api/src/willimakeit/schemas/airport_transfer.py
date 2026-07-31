from pydantic import BaseModel


class AirportTransferEstimate(BaseModel):
    airport_code: str
    arrival_terminal: str | None = None
    departure_terminal: str | None = None
    terminal_transfer_minutes: int
    security_minutes: int
    immigration_minutes: int
    baggage_recheck_minutes: int
    total_required_minutes: int
    self_transfer: bool
    confidence: str
