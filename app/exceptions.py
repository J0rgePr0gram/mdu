class MDUError(Exception):
    """
    Base exception for all errors raised by the MDU.
    """
    pass


class InvalidTimeFormatError(MDUError):
    """
    Raised when a time string does not match the expected HH:MM format.
    """
    pass


class InvalidWorkdayError(MDUError):
    """
    Raised when the configured workday is invalid.
    """
    pass


class InvalidAppointmentDurationError(MDUError):
    """
    Raised when the appointment duration is invalid.
    """
    pass


class ScheduleConflictError(MDUError):
    """
    Raised when schedule data contains overlapping events.
    """
    pass


class NoAvailableSlotsError(MDUError):
    """
    Raised when no available appointment slots can be found.
    """
    pass


class InvalidScheduleConfigurationError(MDUError):
    """
    Raised when the schedule configuration is inconsistent.
    """
    pass

