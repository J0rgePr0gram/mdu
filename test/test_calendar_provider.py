from datetime import datetime
from app.calendar.mock_provider import MockCalendarProvider


def test_mock_provider_returns_empty_events():
    """
    El MockCalendarProvider debe devolver una lista vacía de eventos.
    """
    provider = MockCalendarProvider()
    events = provider.get_events(
        calendar_id="mock_calendar_1",
        target_date="2026-09-11",
    )
    assert isinstance(events, list)
    assert len(events) == 0


def test_mock_provider_slot_is_always_available():
    """
    El MockCalendarProvider debe devolver True en slot_is_available.
    """
    provider = MockCalendarProvider()
    available = provider.slot_is_available(
        calendar_id="mock_calendar_1",
        start_datetime=datetime(2026, 9, 11, 10, 0, 0),
        end_datetime=datetime(2026, 9, 11, 10, 45, 0),
    )
    assert available is True


def test_mock_provider_creates_event():
    """
    El MockCalendarProvider debe simular la creación de un evento.
    """
    provider = MockCalendarProvider()
    event = provider.create_event(
        calendar_id="mock_calendar_1",
        title="Test Event",
        start_datetime=datetime(2026, 9, 11, 10, 0, 0),
        end_datetime=datetime(2026, 9, 11, 10, 45, 0),
    )
    assert "id" in event
    assert "htmlLink" in event
    assert event["id"].startswith("mock_event_")