from unittest.mock import patch

from app.models import (
    CalendarEvent,
    AvailableSlot,
)

from app.engine import find_available_slots_for_service


@patch("app.engine.find_available_slots")
def test_engine_builds_request_and_calls_scheduler(
    mock_scheduler,
    workday,
    service,
):
    """
    The engine should build the reservation request
    and delegate scheduling.
    """

    mock_scheduler.return_value = [
        AvailableSlot(
            start=540,
            end=585,
        )
    ]

    events = [
        CalendarEvent(
            start=780,
            end=840,
        )
    ]

    available_slots = find_available_slots_for_service(
        service=service,
        workday=workday,
        events=events,
    )

    assert available_slots[0].start == 540

    mock_scheduler.assert_called_once()

    called_request = mock_scheduler.call_args.kwargs["request"]

    assert called_request.duration == 45