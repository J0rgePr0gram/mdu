from datetime import datetime
from app.calendar.mock_provider import MockCalendarProvider


def test_create_event():
    provider = MockCalendarProvider()
    event = provider.create_event(
        calendar_id="mock_calendar_1",
        title="Test Event",
        start_datetime=datetime(2026, 9, 15, 10, 0, 0),
        end_datetime=datetime(2026, 9, 15, 10, 45, 0),
    )
    assert "id" in event
    assert "htmlLink" in event
