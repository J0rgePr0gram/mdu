import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import (
    Booking, Resource, Service, Calendar,
    Workday, ReservationRequest,
)


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def workday():
    return Workday(
        start=540,
        end=1140,
        lunch_start=840,
        lunch_end=900,
        interval=15,
    )


@pytest.fixture
def reservation_request():
    return ReservationRequest(duration=45)


@pytest.fixture
def service():
    return Service(id=1, name="Consulta", duration=45)


@pytest.fixture
def resource():
    return Resource(
        id=1,
        name="Dr. Martinez",
        resource_type="person",
        calendar_id=1,
    )


@pytest.fixture
def calendar():
    return Calendar(
        id=1,
        provider="mock",
        external_id="mock_calendar_1",
    )


@pytest.fixture
def booking(db_session):
    from app.repositories.booking_repository import save_booking
    b = Booking(
        id="test-booking-fixture",
        customer_name="Test User",
        service_name="Consulta",
        resource_id=1,
        calendar_id="mock_calendar_1",
        event_id="mock_event_fixture",
        start_datetime=datetime(2026, 9, 15, 10, 0, 0),
        end_datetime=datetime(2026, 9, 15, 10, 45, 0),
        status="active",
    )
    save_booking(db_session, b)
    return b