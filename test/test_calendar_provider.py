from app.models import (
    CalendarEvent,
)

from app.calendar_provider import get_events


def test_calendar_provider_returns_calendar_events():
    """
    The calendar provider should return
    a list of CalendarEvent objects.
    """

    # Act
    events = get_events()

    # Assert
    assert isinstance(events, list)

    assert len(events) == 2

    assert all(
        isinstance(event, CalendarEvent)
        for event in events
    )