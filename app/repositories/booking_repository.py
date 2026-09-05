from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Booking
from app.models_db import BookingDB


def save_booking(
    db: Session,
    booking: Booking,
) -> None:
    """
    Guarda una reserva en la base de datos.
    """

    booking_db = BookingDB(
        id=booking.id,
        customer_name=booking.customer_name,
        service_name=booking.service_name,
        resource_id=booking.resource_id,
        calendar_id=booking.calendar_id,
        event_id=booking.event_id,
        start_datetime=booking.start_datetime,
        end_datetime=booking.end_datetime,
        status=booking.status,
    )

    db.add(booking_db)
    db.commit()


def get_booking(
    db: Session,
    booking_id: str,
) -> Booking:
    """
    Obtiene una reserva desde la base de datos.
    """

    booking_db = (
        db.query(BookingDB)
        .filter(
            BookingDB.id == booking_id
        )
        .first()
    )

    if booking_db is None:
        raise HTTPException(
            status_code=404,
            detail="Reserva no encontrada.",
        )

    return Booking(
        id=booking_db.id,
        customer_name=booking_db.customer_name,
        service_name=booking_db.service_name,
        resource_id=booking_db.resource_id,
        calendar_id=booking_db.calendar_id,
        event_id=booking_db.event_id,
        start_datetime=booking_db.start_datetime,
        end_datetime=booking_db.end_datetime,
        status=booking_db.status,
    )


def update_booking(
    db: Session,
    booking: Booking,
) -> None:
    """
    Actualiza una reserva existente.
    """

    booking_db = (
        db.query(BookingDB)
        .filter(
            BookingDB.id == booking.id
        )
        .first()
    )

    if booking_db is None:
        raise HTTPException(
            status_code=404,
            detail="Reserva no encontrada.",
        )

    booking_db.customer_name = booking.customer_name
    booking_db.service_name = booking.service_name
    booking_db.resource_id = booking.resource_id
    booking_db.calendar_id = booking.calendar_id
    booking_db.event_id = booking.event_id
    booking_db.start_datetime = booking.start_datetime
    booking_db.end_datetime = booking.end_datetime
    booking_db.status = booking.status

    db.commit()


def list_bookings(
    db: Session,
):
    """
    Devuelve todas las reservas.
    """

    bookings_db = (
        db.query(BookingDB)
        .all()
    )

    return [
        Booking(
            id=booking.id,
            customer_name=booking.customer_name,
            service_name=booking.service_name,
            resource_id=booking.resource_id,
            calendar_id=booking.calendar_id,
            event_id=booking.event_id,
            start_datetime=booking.start_datetime,
            end_datetime=booking.end_datetime,
            status=booking.status,
        )
        for booking in bookings_db
    ]


def cancel_booking(
    db: Session,
    booking_id: str,
) -> None:
    """
    Cancela una reserva existente (cambia estado a 'cancelled').
    """
    booking_db = (
        db.query(BookingDB)
        .filter(BookingDB.id == booking_id)
        .first()
    )

    if booking_db is None:
        raise HTTPException(
            status_code=404,
            detail="Reserva no encontrada.",
        )

    # Verificar si ya está cancelada
    if booking_db.status == "cancelled":
        raise HTTPException(
            status_code=409,
            detail="La reserva ya fue cancelada anteriormente.",
        )

    booking_db.status = "cancelled"
    db.commit()