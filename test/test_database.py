import pytest
from datetime import datetime

from app.repositories.booking_repository import (
    save_booking,
    get_booking,
    cancel_booking,
    list_bookings,
)
from app.models import Booking


def test_save_and_get_booking(db_session):
    """Debe guardar y recuperar una reserva."""
    booking = Booking(
        id="test-booking-123",
        customer_name="Test User",
        service_name="Consulta",
        resource_id=1,
        calendar_id="mock_calendar_1",
        event_id="mock_event_123",
        start_datetime=datetime(2026, 9, 15, 10, 0, 0),
        end_datetime=datetime(2026, 9, 15, 10, 45, 0),
        status="active",
    )
    
    save_booking(db_session, booking)
    
    retrieved = get_booking(db_session, "test-booking-123")
    
    assert retrieved.id == "test-booking-123"
    assert retrieved.customer_name == "Test User"
    assert retrieved.status == "active"


def test_cancel_booking(db_session):
    """Debe marcar una reserva como cancelada."""
    booking = Booking(
        id="test-booking-cancel",
        customer_name="Test User",
        service_name="Consulta",
        resource_id=1,
        calendar_id="mock_calendar_1",
        event_id="mock_event_cancel",
        start_datetime=datetime(2026, 9, 15, 11, 0, 0),
        end_datetime=datetime(2026, 9, 15, 11, 45, 0),
        status="active",
    )
    
    save_booking(db_session, booking)
    cancel_booking(db_session, "test-booking-cancel")
    
    retrieved = get_booking(db_session, "test-booking-cancel")
    assert retrieved.status == "cancelled"


def test_list_bookings(db_session):
    """Debe listar todas las reservas."""
    bookings = list_bookings(db_session)
    assert isinstance(bookings, list)