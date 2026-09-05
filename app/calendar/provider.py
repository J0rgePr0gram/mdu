from abc import ABC, abstractmethod
from datetime import datetime


class CalendarProvider(ABC):
    """
    Interfaz común para cualquier proveedor de calendario.
    """

    @abstractmethod
    def slot_is_available(
        self,
        calendar_id: str,
        start_datetime: datetime,
        end_datetime: datetime,
    ) -> bool:
        pass

    @abstractmethod
    def create_event(
        self,
        calendar_id: str,
        title: str,
        start_datetime: datetime,
        end_datetime: datetime,
    ):
        pass

    @abstractmethod
    def delete_event(
        self,
        calendar_id: str,
        event_id: str,
    ):
        pass

    @abstractmethod
    def update_event(
        self,
        calendar_id: str,
        event_id: str,
        start_datetime: datetime,
        end_datetime: datetime,
    ):
        pass