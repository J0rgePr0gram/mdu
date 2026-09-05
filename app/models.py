from dataclasses import dataclass
from datetime import datetime

from app.exceptions import (
    InvalidWorkdayError,
    InvalidAppointmentDurationError,
    ScheduleConflictError,
)

@dataclass
class Workday:
    """
    Represents a resource's working schedule.
    """

    start: int
    end: int
    lunch_start: int
    lunch_end: int
    interval: int

    def __post_init__(self):
        """
        Validate the workday after creation.
        """

        if self.start >= self.end:
            raise InvalidWorkdayError(
                "Workday start time must be earlier than end time."
            )


@dataclass
class CalendarEvent:
    """
    Represents a busy period in a calendar.
    """

    start: int
    end: int

    def __post_init__(self):
        """
        Validate the calendar event.
        """

        if self.start >= self.end:
            raise ScheduleConflictError(
                "Calendar event start time must be earlier than end time."
            )


@dataclass
class ReservationRequest:
    """
    Represents a client's reservation request.
    """

    duration: int

    def __post_init__(self):
        """
        Validate the reservation request.
        """

        if self.duration <= 0:
            raise InvalidAppointmentDurationError(
                "Appointment duration must be greater than zero."
            )


@dataclass
class AvailableSlot:
    """
    Represents an available appointment slot.
    """

    start: int
    end: int

    def __post_init__(self):
        """
        Validate the available slot.
        """

        if self.start >= self.end:
            raise ScheduleConflictError(
                "Available slot start time must be earlier than end time."
            )


@dataclass
class Service:
    """
    Represents a service that can be booked.
    """

    id: int
    name: str
    duration: int


@dataclass
class Resource:
    """
    Represents a bookable resource.
    """

    id: int
    name: str
    resource_type: str
    calendar_id: int

    
@dataclass
class Calendar:
    """
    Represents an external or internal calendar
    associated with a bookable resource.
    """

    id: int
    provider: str
    external_id: str
@dataclass
class Booking:
    """
    Represents a confirmed booking.
    """

    id: str
    customer_name: str
    service_name: str
    resource_id: int
    calendar_id: str
    event_id: str
    start_datetime: datetime
    end_datetime: datetime
    status: str = "active"


