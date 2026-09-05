from datetime import datetime, timedelta

from app.models import (
    Workday,
    CalendarEvent,
    ReservationRequest,
    AvailableSlot,
    Service,
    Resource,
    Calendar,
)

from app.scheduler import find_available_slots
from app.calendar.google_provider import GoogleCalendarProvider

calendar_provider = GoogleCalendarProvider()


def find_available_slots_for_resource(
    resource: Resource,
    service: Service,
    workday: Workday,
    events: list[CalendarEvent],
) -> list[AvailableSlot]:
    """
    Busca todos los horarios disponibles para un recurso
    según el servicio solicitado.

    El recurso puede representar:
    - una persona
    - una sala
    - un vehículo
    - un equipo
    - cualquier otro recurso reservable

    El motor utiliza la duración del servicio,
    el horario de trabajo y los eventos ocupados
    para calcular los horarios disponibles.
    """

    # Crea una solicitud de reserva utilizando
    # la duración definida para el servicio.
    reservation_request = ReservationRequest(
        duration=service.duration,
    )

    # Delega el cálculo de los horarios disponibles
    # al algoritmo principal de planificación.
    available_slots = find_available_slots(
        workday=workday,
        events=events,
        request=reservation_request,
    )

    return available_slots


def book_appointment(
    resource: Resource,
    calendar: Calendar,
    service: Service,
    customer_name: str,
    start_datetime: datetime,
):
    """
    Crea una reserva para un recurso.

    El recurso puede representar cualquier elemento
    que pueda ser reservado.

    Por ahora, la creación del evento se realiza
    mediante Google Calendar.
    """

    # Calcula la fecha y hora de término
    # utilizando la duración definida por el servicio.
    end_datetime = (
        start_datetime
        + timedelta(minutes=service.duration)
    )

    # Construye el título del evento
    # que se mostrará en el calendario.
    title = (
        f"{customer_name} - "
        f"{service.name}"
    )

    # Crea el evento en el calendario asociado
    # al recurso y devuelve el evento creado.
    return calendar_provider.create_event(
        calendar_id=calendar.external_id,
        title=title,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
    )