from fastapi.testclient import TestClient

from willimakeit.main import app


class FakeAgentResult:
    text = "I found flight QR 4818 from Malta International Airport to Paris Charles de Gaulle."


class FakeAgent:
    def __init__(self) -> None:
        self.received_message: str | None = None

    async def run(self, message: str) -> FakeAgentResult:
        self.received_message = message
        return FakeAgentResult()


def test_assistant_ask_returns_completed_response() -> None:
    fake_agent = FakeAgent()
    with TestClient(app) as client:
        app.state.assistant_agent = fake_agent
        response = client.post(
            "/assistant/ask",
            json={"message": "Check my flight"},
        )

    assert response.status_code == 200
    assert response.json()["status"] == "completed"
    assert "QR 4818" in response.json()["message"]
    assert fake_agent.received_message == "Check my flight"
