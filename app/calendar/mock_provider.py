from datetime import datetime, date
from app.calendar.provider import CalendarProvider


class MockCalendarProvider(CalendarProvider):
    """
    Proveedor de calendario simulado para pruebas sin Google Calendar.
    """

    def get_events(
        self,
        calendar_id: str,
        target_date: date | None = None,
    ) -> list:
        # Simula que no hay eventos ocupados
        return []

    def slot_is_available(
        self,
        calendar_id: str,
        start_datetime: datetime,
        end_datetime: datetime,
        exclude_event_id: str = None,
    ) -> bool:
        # Simula que siempre hay disponibilidad
        return True

    def create_event(
        self,
        calendar_id: str,
        title: str,
        start_datetime: datetime,
        end_datetime: datetime,
    ):
        return {
            "id": f"mock_event_{start_datetime.timestamp()}",
            "htmlLink": "https://mock-calendar.example.com/event",
        }

    def delete_event(
        self,
        calendar_id: str,
        event_id: str,
    ) -> bool:
        return True

    def update_event(
        self,
        calendar_id: str,
        event_id: str,
        start_datetime: datetime,
        end_datetime: datetime,
    ):
        return {
            "id": event_id,
            "htmlLink": "https://mock-calendar.example.com/updated_event",
        }