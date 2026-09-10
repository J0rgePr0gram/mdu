from datetime import date, datetime  # Agregar datetime
from fastapi import HTTPException  # Agregar HTTPException

from app.calendar.google_provider import GoogleCalendarProvider
from app.engine import find_available_slots_for_resource
from app.models import (
    Resource,
    Calendar,
    Service,
    Workday,
)

calendar_provider = GoogleCalendarProvider()


def get_available_slots(
    resource: Resource,
    calendar: Calendar,
    service: Service,
    target_date: date,
):
    """
    Obtiene todos los horarios disponibles para un recurso
    en una fecha determinada considerando el servicio solicitado.
    """

    print("\n========== CONSULTANDO DISPONIBILIDAD ==========")

    print("Recurso:", resource.name)
    print("Tipo:", resource.resource_type)

    print("Servicio:", service.name)
    print("Duración:", service.duration, "minutos")

    print("Proveedor:", calendar.provider)
    print("Calendario:", calendar.external_id)

    # --------------------------------------------------------
    # 1. Definir el horario laboral del recurso
    # --------------------------------------------------------

    workday = Workday(
        start=540,
        end=1140,
        lunch_start=840,
        lunch_end=900,
        interval=15,
    )

    # --------------------------------------------------------
    # 2. Obtener los eventos ocupados del calendario
    # --------------------------------------------------------

    events = calendar_provider.get_events(
        calendar_id=calendar.external_id,
        target_date=target_date,
    )

    print("Eventos encontrados:", events)

    # --------------------------------------------------------
    # 3. Delegar el cálculo de disponibilidad al motor
    # --------------------------------------------------------

    available_slots = find_available_slots_for_resource(
        resource=resource,
        service=service,
        workday=workday,
        events=events,
    )

    print(
        "Horarios disponibles:",
        len(available_slots),
    )

    # --------------------------------------------------------
    # 4. Convertir los horarios al formato HH:MM
    # --------------------------------------------------------

    return [
        {
            "start": f"{slot.start // 60:02d}:{slot.start % 60:02d}",
            "end": f"{slot.end // 60:02d}:{slot.end % 60:02d}",
        }
        for slot in available_slots
    ]


def validate_booking_datetime(start_datetime: datetime) -> None:
    """
    Valida que la fecha y hora de la reserva sea válida.
    - No puede ser en el pasado.
    - No puede ser antes de la fecha actual.
    """
    now = datetime.now()
    
    if start_datetime < now:
        raise HTTPException(
            status_code=400,
            detail="No se puede reservar en el pasado."
        )