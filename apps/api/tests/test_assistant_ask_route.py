from datetime import date

from fastapi.testclient import TestClient

from willimakeit.main import app
from willimakeit.schemas.flight import Airport, FlightSchedule


class FakeFlightService:
    def __init__(self) -> None:
        self.received_flight_number: str | None = None
        self.received_flight_date: date | None = None

    async def find_flight(
        self,
        flight_number: str,
        flight_date: date,
    ) -> FlightSchedule:
        self.received_flight_number = flight_number
        self.received_flight_date = flight_date

        return FlightSchedule(
            flight_number="QR 4818",
            flight_date=date(2026, 7, 15),
            departure_airport=Airport(
                iata="MLA",
                name="Malta International Airport",
            ),
            arrival_airport=Airport(
                iata="CDG",
                name="Paris Charles de Gaulle",
            ),
        )


def test_assistant_ask_uses_flight_service() -> None:
    fake_service = FakeFlightService()
    with TestClient(app) as client:
        app.state.flight_service = fake_service
        response = client.post(
            "/assistant/ask",
            json={"message": "Check my flight"},
        )

    assert response.status_code == 200
    assert response.json()["status"] == "accepted"
    assert "QR 4818" in response.json()["message"]
    assert fake_service.received_flight_number == "QR4818"
    assert fake_service.received_flight_date == date(2026, 7, 15)
