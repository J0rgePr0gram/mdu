import pytest


from app.models import (
    Workday,
    ReservationRequest,
    Service,
)


@pytest.fixture
def service():
    """
    Creates a standard service for tests.
    """

    return Service(
        id=1,
        name="Consulta General",
        duration=45,
    )


@pytest.fixture
def workday():
    """
    Creates a standard workday for tests.
    """

    return Workday(
        start=540,
        end=1140,
        lunch_start=840,
        lunch_end=900,
        interval=15,
    )


@pytest.fixture
def reservation_request():
    """
    Creates a standard reservation request for tests.
    """

    return ReservationRequest(
        duration=45,
    )