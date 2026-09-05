from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session
import uuid
import logging

from app.models import Booking, Service, Resource, Calendar
from app.repositories.booking_repository import save_booking
from app.calendar.google_provider import GoogleCalendarProvider

logger = logging.getLogger(__name__)
calendar_provider = GoogleCalendarProvider()


def book_appointment(
    db: Session,
    customer_name: str,
    service: Service,
    resource: Resource,
    calendar: Calendar,
    start_datetime: datetime,
) -> dict:
    """
    Gestiona la creación completa de una reserva con consistencia transaccional.
    """
    # Calcular end_datetime
    end_datetime = start_datetime + timedelta(minutes=service.duration)
    
    # 1. Verificar disponibilidad en Google Calendar
    logger.info(f"Verificando disponibilidad para {resource.name} a las {start_datetime}")
    available = calendar_provider.slot_is_available(
        calendar_id=calendar.external_id,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
    )
    
    if not available:
        logger.warning(f"Horario ocupado: {start_datetime} - {end_datetime}")
        raise HTTPException(
            status_code=409,
            detail="Este horario ya está reservado.",
        )
    
    # 2. Crear evento en Google Calendar
    try:
        logger.info(f"Creando evento en Google Calendar para {customer_name}")
        event = calendar_provider.create_event(
            calendar_id=calendar.external_id,
            title=f"{customer_name} - {service.name}",
            start_datetime=start_datetime,
            end_datetime=end_datetime,
        )
        logger.info(f"Evento creado con ID: {event['id']}")
    except Exception as e:
        logger.error(f"Error al crear evento en Google Calendar: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear evento en Google Calendar: {str(e)}"
        )
    
    # 3. Crear reserva en SQLite
    booking = Booking(
        id=str(uuid.uuid4()),
        customer_name=customer_name,
        service_name=service.name,
        resource_id=resource.id,
        calendar_id=calendar.external_id,
        event_id=event["id"],
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        status="active",
    )
    
    try:
        save_booking(db, booking)
        logger.info(f"Reserva guardada en SQLite con ID: {booking.id}")
    except Exception as e:
        logger.error(f"Error al guardar reserva en SQLite: {e}")
        # Intentar eliminar el evento de Google Calendar para compensar
        try:
            calendar_provider.delete_event(calendar.external_id, event["id"])
            logger.info(f"Evento {event['id']} eliminado de Google Calendar por fallo en SQLite")
        except Exception as delete_error:
            logger.error(f"Error al eliminar evento de compensación: {delete_error}")
        
        raise HTTPException(
            status_code=500,
            detail=f"Error al guardar la reserva: {str(e)}"
        )
    
    logger.info(f"Reserva completada exitosamente: {booking.id}")
    
    return {
        "status": "success",
        "booking_id": booking.id,
        "customer": booking.customer_name,
        "service": booking.service_name,
        "resource": resource.name,
        "date": booking.start_datetime.date(),
        "start": booking.start_datetime.time(),
        "end": booking.end_datetime.time(),
        "calendar_link": event["htmlLink"],
    }