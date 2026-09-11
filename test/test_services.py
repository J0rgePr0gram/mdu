import pytest
from datetime import datetime
from unittest.mock import patch

from app.booking_service import book_appointment
from app.cancellation_service import cancel_appointment
from app.reschedule_service import reschedule_appointment


def test_book_appointment_success(db_session, service, resource, calendar):
    with patch("app.booking_service.calendar_provider") as mock_provider:
        mock_provider.slot_is_available.return_value = True
        mock_provider.create_event.return_value = {
            "id": "mock_event_123",
            "htmlLink": "https://mock.com/event",
        }
        result = book_appointment(
            db=db_session,
            customer_name="Test User",
            service=service,
            resource=resource,
            calendar=calendar,
            start_datetime=datetime(2026, 9, 15, 10, 0, 0),
        )
        assert result["status"] == "success"
        assert "booking_id" in result


def test_cancel_appointment_success(db_session, booking):
    with patch("app.cancellation_service.calendar_provider") as mock_provider:
        mock_provider.delete_event.return_value = True
        result = cancel_appointment(
            db=db_session,
            booking_id=booking.id,
        )
        assert "message" in result
        assert "cancelada" in result["message"].lower()


def test_reschedule_appointment_success(db_session, booking):
    with patch("app.reschedule_service.calendar_provider") as mock_provider:
        mock_provider.slot_is_available.return_value = True
        mock_provider.update_event.return_value = {
            "id": booking.event_id,
            "htmlLink": "https://mock.com/updated",
        }
        result = reschedule_appointment(
            db=db_session,
            booking_id=booking.id,
            start_datetime=datetime(2026, 9, 15, 15, 0, 0),
        )
        assert "message" in result
        assert "reagendada" in result["message"].lower()