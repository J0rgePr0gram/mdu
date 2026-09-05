from datetime import datetime, timedelta, date
from zoneinfo import ZoneInfo

from googleapiclient.discovery import build

from app.google_auth import get_credentials
from app.models import CalendarEvent


def get_events(
    calendar_id: str,
    target_date: date | None = None,
) -> list[CalendarEvent]:
    """
    Obtiene los eventos ocupados de un calendario específico
    para una fecha determinada.

    El calendario puede pertenecer a cualquier recurso reservable,
    por ejemplo:
    - una persona
    - una sala
    - un vehículo
    - un equipo
    - cualquier otro recurso

    El motor no necesita saber qué representa el calendario.
    Solo necesita recibir los períodos que están ocupados.
    """

    # Definimos la zona horaria utilizada por el sistema.
    # Por ahora trabajamos con la zona horaria de Chile.
    chile_tz = ZoneInfo("America/Santiago")

    # Obtiene las credenciales válidas de Google.
    creds = get_credentials()

    # Construye el cliente de la API de Google Calendar.
    service = build(
        "calendar",
        "v3",
        credentials=creds,
    )

    # Si no se proporciona una fecha,
    # utilizamos la fecha actual en horario de Chile.
    if target_date is None:
        target_date = datetime.now(
            chile_tz
        ).date()

    # Define el inicio del día solicitado.
    start_of_day = datetime.combine(
        target_date,
        datetime.min.time(),
        tzinfo=chile_tz,
    )

    # Define el final del día solicitado.
    # Se utiliza el día siguiente como límite superior
    # para incluir todos los eventos del día.
    end_of_day = (
        start_of_day
        + timedelta(days=1)
    )

    # Consulta los eventos del calendario indicado.
    events_result = (
        service.events()
        .list(
            calendarId=calendar_id,
            timeMin=start_of_day.isoformat(),
            timeMax=end_of_day.isoformat(),
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    # Obtiene la lista de eventos.
    # Si el calendario no tiene eventos,
    # se obtiene una lista vacía.
    google_events = events_result.get(
        "items",
        []
    )

    # Aquí almacenaremos los eventos convertidos
    # al modelo interno del motor.
    events = []

    for event in google_events:

        # Ignoramos los eventos de día completo.
        # El motor actualmente trabaja con horarios
        # específicos de inicio y término.
        if "dateTime" not in event["start"]:
            continue

        # Convierte la fecha y hora de inicio
        # de Google Calendar a un objeto datetime.
        start_dt = datetime.fromisoformat(
            event["start"]["dateTime"]
        )

        # Convierte la fecha y hora de término
        # de Google Calendar a un objeto datetime.
        end_dt = datetime.fromisoformat(
            event["end"]["dateTime"]
        )

        # Convierte la hora de inicio a minutos
        # desde el comienzo del día.
        start_minutes = (
            start_dt.hour * 60
            + start_dt.minute
        )

        # Convierte la hora de término a minutos
        # desde el comienzo del día.
        end_minutes = (
            end_dt.hour * 60
            + end_dt.minute
        )

        # Convierte el evento de Google Calendar
        # al modelo interno que utiliza el motor.
        events.append(
            CalendarEvent(
                start=start_minutes,
                end=end_minutes,
            )
        )

    # Devuelve únicamente los períodos ocupados
    # que el motor necesita para calcular
    # los horarios disponibles.
    return events