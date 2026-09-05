from app.scheduler import find_available_slots

from app.models import (
    CalendarEvent,
)
from app.scheduler import find_available_slots


def test_scheduler_finds_available_slots(workday, reservation_request):
    """
    The scheduler should return the expected first and last available slots.
    """


    events = [
        CalendarEvent(
            start=780,
            end=840,
        ),
        CalendarEvent(
            start=990,
            end=1035,
        ),
    ]


    # Act
    available_slots = find_available_slots(
        workday=workday,
        events=events,
        request=reservation_request,
    )

    # Assert
    assert len(available_slots) == 23

    assert available_slots[0].start == 540
    assert available_slots[0].end == 585

    assert available_slots[-1].start == 1095
    assert available_slots[-1].end == 1140

def test_scheduler_respects_lunch_break(workday, reservation_request):
    """
    The scheduler must never return slots that start during lunch time.
    """


    events = [
        CalendarEvent(
            start=780,
            end=840,
        ),
        CalendarEvent(
            start=990,
            end=1035,
        ),
    ]


    # Act
    available_slots = find_available_slots(
        workday=workday,
        events=events,
        request=reservation_request,
    )

    # Assert
    for slot in available_slots:
        assert not (
            workday.lunch_start <= slot.start < workday.lunch_end
        )

def test_scheduler_without_events(workday, reservation_request):
    """
    The scheduler should return every possible slot
    when the calendar has no events.
    """

    
    events = []


    # Act
    available_slots = find_available_slots(
        workday=workday,
        events=events,
        request=reservation_request,
    )
    
    # Assert
    assert len(available_slots) == 32

    assert available_slots[0].start == 540
    assert available_slots[0].end == 585

    assert available_slots[-1].start == 1095
    assert available_slots[-1].end == 1140   

def test_scheduler_returns_empty_when_day_is_full(workday, reservation_request):
    """
    The scheduler should return no available slots
    when the entire workday is occupied.
    """


    events = [
        CalendarEvent(
            start=540,
            end=1140,
        )
    ]

   
    # Act
    available_slots = find_available_slots(
        workday=workday,
        events=events,
        request=reservation_request,
    )

    # Assert
    assert available_slots == []