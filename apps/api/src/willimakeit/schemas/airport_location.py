from pydantic import BaseModel


class AirportLocation(BaseModel):
    airport_code: str
    latitude: float
    longitude: float
