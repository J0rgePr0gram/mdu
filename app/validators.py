from datetime import datetime

from fastapi import HTTPException


def validate_booking_datetime(
    start_datetime: datetime,
):
    """
    Impide crear reservas en fechas pasadas.
    """

    now = datetime.now(start_datetime.tzinfo)

    if start_datetime < now:

        raise HTTPException(
            status_code=400,
            detail="No se puede reservar en una fecha u hora pasada.",
        )