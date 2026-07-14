from fastapi import FastAPI
from datetime import date
from pydantic import BaseModel

app = FastAPI(title="Will I Make It API", version="0.1.0")

class ConnectionCheckRequest(BaseModel):
    inbound_flight: str
    inbound_date: date
    outbound_flight: str
    outbound_date: date

@app.get("/health")
async def health() -> dict[str,str]:
  return {"status": "ok"}


@app.post("/connections/check")
async def check_connection(item: ConnectionCheckRequest) -> ConnectionCheckRequest:
  return item