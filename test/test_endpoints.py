from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """El endpoint raíz debe devolver un mensaje."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_get_available_slots():
    """Debe devolver slots disponibles para un recurso y servicio."""
    response = client.get(
        "/available-slots",
        params={
            "resource_id": 1,
            "service_name": "Consulta",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "slots" in data
    assert isinstance(data["slots"], list)


@patch("app.booking_service.calendar_provider")
def test_create_booking(mock_provider):
    """Debe crear una reserva correctamente (con mock)."""
    mock_provider.slot_is_available.return_value = True
    mock_provider.create_event.return_value = {
        "id": "mock_event_test",
        "htmlLink": "https://mock.com/event",
    }
    
    response = client.post(
        "/book",
        json={
            "customer_name": "Test User",
            "service_name": "Consulta",
            "resource_id": 1,
            "date": "2027-06-15",
            "start_time": "08:00:00",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "booking_id" in data