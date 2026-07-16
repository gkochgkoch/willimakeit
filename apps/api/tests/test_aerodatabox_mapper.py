import json
from datetime import date
from pathlib import Path

from willimakeit.providers.aerodatabox_mapper import map_flight_schedule

FIXTURES = Path(__file__).parent / "fixtures" / "aerodatabox"


def test_map_flight_schedule() -> None:
    raw = json.loads((FIXTURES / "scheduled.json").read_text(encoding="utf-8"))[0]

    result = map_flight_schedule(raw, flight_date=date(2026, 7, 15))

    assert result.flight_number == "QR 4818"
    assert result.flight_date == date(2026, 7, 15)
    assert result.departure_airport.iata == "MLA"
    assert result.departure_airport.icao == "LMML"
    assert result.arrival_airport.name == "Paris Charles de Gaulle"
    assert result.scheduled_departure_utc is not None
    assert result.airline_iata == "QR"
