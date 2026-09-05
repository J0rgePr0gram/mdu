from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session
import logging

from app.repositories.booking_repository import get_booking, update_booking
from app.repositories.service_repository import get_service
from app.calendar.google_provider import GoogleCalendarProvider

logger = logging.getLogger(__name__)


def reschedule_appointment(
    db: Session,
    booking_id: str,
    start_datetime: datetime,
) -> dict:
    """
    Reagenda una reserva existente con consistencia transaccional.
    """
    # 1. Obtener reserva de SQLite
    booking = get_booking(db, booking_id)
    logger.info(f"Reserva obtenida: {booking_id}, estado: {booking.status}")
    
    # Verificar si está cancelada
    if booking.status == "cancelled":
        logger.warning(f"Intento de reagendar reserva cancelada: {booking_id}")
        raise HTTPException(
            status_code=409,
            detail="No se puede reagendar una reserva cancelada.",
        )
    
    # Guardar valores originales por si falla
    original_start = booking.start_datetime
    original_end = booking.end_datetime
    
    # 2. Calcular nueva hora de fin
    service = get_service(booking.service_name)
    end_datetime = start_datetime + timedelta(minutes=service.duration)
    logger.info(f"Nuevo horario: {start_datetime} - {end_datetime}")
    
    # 3. Validar disponibilidad en Google Calendar (excluyendo el evento actual)
    calendar_provider = GoogleCalendarProvider()
    available = calendar_provider.slot_is_available(
        calendar_id=booking.calendar_id,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        exclude_event_id=booking.event_id,  # Ahora funciona con el nuevo método
    )
    
    if not available:
        logger.warning(f"Nuevo horario ocupado: {start_datetime} - {end_datetime}")
        raise HTTPException(
            status_code=409,
            detail="El nuevo horario no está disponible.",
        )
    
    # 4. Actualizar evento en Google Calendar
    try:
        calendar_provider.update_event(
            calendar_id=booking.calendar_id,
            event_id=booking.event_id,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
        )
        logger.info(f"Evento {booking.event_id} actualizado en Google Calendar")
    except Exception as e:
        logger.error(f"Error al actualizar evento en Google Calendar: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al actualizar el evento: {str(e)}"
        )
    
    # 5. Actualizar SQLite
    try:
        booking.start_datetime = start_datetime
        booking.end_datetime = end_datetime
        update_booking(db, booking)
        logger.info(f"Reserva {booking_id} actualizada en SQLite")
    except Exception as e:
        logger.error(f"Error al actualizar reserva en SQLite: {e}")
        # Intentar revertir el evento de Google Calendar
        try:
            calendar_provider.update_event(
                calendar_id=booking.calendar_id,
                event_id=booking.event_id,
                start_datetime=original_start,
                end_datetime=original_end,
            )
            logger.info(f"Evento revertido a horario original en Google Calendar")
        except Exception as revert_error:
            logger.error(f"Error al revertir evento: {revert_error}")
        
        raise HTTPException(
            status_code=500,
            detail=f"Error al actualizar la reserva: {str(e)}"
        )
    
    logger.info(f"RESERVA REAGENDADA: {booking_id}")
    
    return {
        "message": "Reserva reagendada exitosamente",
        "booking_id": booking.id,
        "new_start": start_datetime.isoformat(),
        "new_end": end_datetime.isoformat(),
    }