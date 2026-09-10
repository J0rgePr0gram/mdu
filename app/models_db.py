from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class BookingDB(Base):
    __tablename__ = "bookings"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
    )

    customer_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    service_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    resource_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    calendar_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    event_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    start_datetime: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    end_datetime: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default="active",
    )


class ResourceDB(Base):
    __tablename__ = "resources"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    resource_type: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )


class ServiceDB(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )

    duration: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )


class CalendarDB(Base):
    __tablename__ = "calendars"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    resource_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    provider: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    external_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
