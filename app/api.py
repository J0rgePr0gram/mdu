from datetime import datetime, date, time
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models_db import BookingDB

from app.availability_service import get_available_slots
from app.booking_service import book_appointment
from app.reschedule_service import reschedule_appointment

from app.repositories.resource_repository import get_resource
from app.repositories.service_repository import get_service
from app.repositories.calendar_repository import get_calendar_for_resource
from app.repositories.booking_repository import get_booking

from app.cancellation_service import cancel_appointment
from app.auth import verify_api_key


# ============================================================
# CREAR EL ROUTER
# ============================================================

router = APIRouter()


# ============================================================
# MODELOS DE REQUEST
# ============================================================

class BookingRequest(BaseModel):
    customer_name: str
    service_name: str
    resource_id: int
    date: date
    start_time: time


class RescheduleRequest(BaseModel):
    date: date
    start_time: time


# ============================================================
# RUTA PRINCIPAL
# ============================================================

@router.get("/")
def root():
    return {
        "message": "MDU Scheduler API"
    }


# ============================================================
# DISPONIBILIDAD
# ============================================================

@router.get("/available-slots", dependencies=[Depends(verify_api_key)])
def available_slots(
    resource_id: int,
    service_name: str,
    target_date: date | None = None,
):
    if target_date is None:
        target_date = date.today()

    resource = get_resource(resource_id)
    service = get_service(service_name)

    try:
        calendar = get_calendar_for_resource(resource.id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    slots = get_available_slots(
        resource=resource,
        calendar=calendar,
        service=service,
        target_date=target_date,
    )

    return {
        "resource_id": resource.id,
        "resource": resource.name,
        "resource_type": resource.resource_type,
        "service": service.name,
        "duration": service.duration,
        "date": target_date,
        "slots": slots,
    }


# ============================================================
# CREAR RESERVA
# ============================================================

@router.post("/book", dependencies=[Depends(verify_api_key)])
def book(
    request: BookingRequest,
    db: Session = Depends(get_db),
):
    print("\n========== NUEVA RESERVA ==========")
    print("Datos recibidos:", request)

    resource = get_resource(request.resource_id)
    service = get_service(request.service_name)

    try:
        calendar = get_calendar_for_resource(request.resource_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    start_datetime = datetime.combine(
        request.date,
        request.start_time,
    )

    result = book_appointment(
        db=db,
        customer_name=request.customer_name,
        service=service,
        resource=resource,
        calendar=calendar,
        start_datetime=start_datetime,
    )

    return result


# ============================================================
# OBTENER RESERVA
# ============================================================

@router.get("/booking/{booking_id}", dependencies=[Depends(verify_api_key)])
def get_booking_endpoint(
    booking_id: str,
    db: Session = Depends(get_db),
):
    """
    Obtiene una reserva por su ID.
    """
    try:
        booking = get_booking(db, booking_id)
        return booking
    except HTTPException as e:
        raise e


# ============================================================
# CANCELAR RESERVA
# ============================================================

@router.delete("/booking/{booking_id}", dependencies=[Depends(verify_api_key)])
def cancel_booking_endpoint(
    booking_id: str,
    db: Session = Depends(get_db),
):
    """
    Cancela una reserva existente.
    - Marca la reserva como 'cancelled' en la base de datos.
    - Elimina el evento correspondiente en Google Calendar.
    """
    try:
        result = cancel_appointment(
            db=db,
            booking_id=booking_id,
        )
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al cancelar la reserva: {str(e)}"
        )


# ============================================================
# REAGENDAR RESERVA
# ============================================================

@router.patch("/booking/{booking_id}", dependencies=[Depends(verify_api_key)])
def reschedule_booking_endpoint(
    booking_id: str,
    request: RescheduleRequest,
    db: Session = Depends(get_db),
):
    """
    Reagenda una reserva existente.
    """
    try:
        start_datetime = datetime.combine(
            request.date,
            request.start_time,
        )

        return reschedule_appointment(
            db=db,
            booking_id=booking_id,
            start_datetime=start_datetime,
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al reagendar la reserva: {str(e)}"
        )