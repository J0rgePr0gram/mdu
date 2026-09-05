from fastapi import HTTPException

from app.datasource.memory_datasource import (
    RESOURCES,
    CALENDARS,
)
from app.models import Calendar


def get_calendar_for_resource(
    resource_id: int,
) -> Calendar:
    """
    Obtiene el calendario asociado a un recurso.
    """

    resource = RESOURCES.get(
        resource_id
    )

    if resource is None:

        raise HTTPException(
            status_code=404,
            detail="Recurso no encontrado.",
        )

    calendar = CALENDARS.get(
        resource.calendar_id
    )

    if calendar is None:

        raise HTTPException(
            status_code=404,
            detail="Calendario no encontrado.",
        )

    return calendar