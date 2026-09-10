import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from googleapiclient.errors import HttpError

from app.calendar.mock_provider import MockCalendarProvider
from app.repositories.booking_repository import get_booking, cancel_booking

logger = logging.getLogger(__name__)
calendar_provider = MockCalendarProvider()


def cancel_appointment(
    db: Session,
    booking_id: str,
) -> dict:
    """
    Cancela una reserva existente.
    """
    # 1. Obtener reserva de SQLite
    booking = get_booking(db, booking_id)
    
    # Verificar si ya está cancelada
    if booking.status == "cancelled":
        raise HTTPException(
            status_code=409,
            detail="La reserva ya fue cancelada anteriormente.",
        )
    
    # 2. Eliminar evento de Google Calendar
    try:
        calendar_provider.delete_event(booking.calendar_id, booking.event_id)
        logger.info(f"Evento {booking.event_id} eliminado de Google Calendar")
    except Exception as e:
        logger.error(f"Error al eliminar evento de Google Calendar: {e}")
        # No lanzamos excepción aquí, continuamos para marcar como cancelada en SQLite
        # pero registramos el error para monitoreo
    
    # 3. Marcar como cancelada en SQLite
    try:
        cancel_booking(db, booking_id)
        logger.info(f"Reserva {booking_id} marcada como cancelada en SQLite")
    except Exception as e:
        logger.error(f"Error al marcar reserva como cancelada en SQLite: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al cancelar la reserva: {str(e)}"
        )
    
    return {"message": "Reserva cancelada exitosamente"}