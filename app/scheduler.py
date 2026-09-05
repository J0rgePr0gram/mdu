from app.models import (
    Workday,
    CalendarEvent,
    ReservationRequest,
    AvailableSlot,
)


def find_available_slots(
    workday: Workday,
    events: list[CalendarEvent],
    request: ReservationRequest,
) -> list[AvailableSlot]:
    """
    Encuentra todos los horarios disponibles para una jornada laboral,
    considerando los eventos existentes, el horario de almuerzo
    y la duración del servicio solicitado.
    """

    # Crear el evento correspondiente al horario de almuerzo
    lunch_event = CalendarEvent(
        start=workday.lunch_start,
        end=workday.lunch_end,
    )

    # Copiar los eventos existentes para no modificar la lista original
    all_events = events.copy()

    # Agregar el almuerzo como un período ocupado
    all_events.append(lunch_event)

    # Ordenar todos los eventos según su hora de inicio
    all_events.sort(
        key=lambda event: event.start
    )

    # Buscar bloques de tiempo libres
    free_blocks = []

    # Comenzamos desde el inicio de la jornada laboral
    current_start = workday.start

    for event in all_events:

        # Si existe espacio libre antes del evento
        if current_start < event.start:

            free_blocks.append(
                (
                    current_start,
                    event.start,
                )
            )

        # Avanzamos el inicio actual hasta el final
        # del evento si este termina más tarde
        current_start = max(
            current_start,
            event.end,
        )

    # Revisar si queda un bloque libre
    # después del último evento hasta el final de la jornada
    if current_start < workday.end:

        free_blocks.append(
            (
                current_start,
                workday.end,
            )
        )

    # Lista final de horarios disponibles
    available_slots = []

    # Analizar cada bloque libre
    for block_start, block_end in free_blocks:

        # Última hora posible en la que puede comenzar
        # el servicio para que termine dentro del bloque
        latest_start = (
            block_end - request.duration
        )

        # Comenzar desde el inicio del bloque libre
        current = block_start

        # Generar horarios según el intervalo configurado
        while current <= latest_start:

            # Agregar el horario disponible
            available_slots.append(
                AvailableSlot(
                    start=current,
                    end=current + request.duration,
                )
            )

            # Avanzar según el intervalo de la jornada
            current += workday.interval

    # Devolver todos los horarios disponibles
    return available_slots