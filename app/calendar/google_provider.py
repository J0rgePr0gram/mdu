from datetime import datetime
from zoneinfo import ZoneInfo

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from app.google_auth import get_credentials

from app.calendar.provider import CalendarProvider


CHILE_TIMEZONE = "America/Santiago"


class GoogleCalendarProvider(
    CalendarProvider
):
    """
    Implementación de CalendarProvider
    para Google Calendar.
    """

    def _ensure_chile_timezone(
        self,
        value: datetime,
    ) -> datetime:

        chile_tz = ZoneInfo(
            CHILE_TIMEZONE
        )

        if value.tzinfo is None:
            return value.replace(
                tzinfo=chile_tz
            )

        return value.astimezone(
            chile_tz
        )

    def _get_calendar_service(self):

        creds = get_credentials()

        return build(
            "calendar",
            "v3",
            credentials=creds,
        )

    def slot_is_available(
        self,
        calendar_id: str,
        start_datetime: datetime,
        end_datetime: datetime,
        exclude_event_id: str = None,  # <--- AGREGADO
    ) -> bool:
        """
        Verifica si un slot está disponible en Google Calendar.
        Si se proporciona exclude_event_id, se ignora ese evento (para reagendamientos).
        """

        start_datetime = (
            self._ensure_chile_timezone(
                start_datetime
            )
        )

        end_datetime = (
            self._ensure_chile_timezone(
                end_datetime
            )
        )

        service = (
            self._get_calendar_service()
        )

        try:

            events_result = (
                service.events()
                .list(
                    calendarId=calendar_id,
                    timeMin=start_datetime.isoformat(),
                    timeMax=end_datetime.isoformat(),
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )

            events = events_result.get(
                "items",
                []
            )

            for event in events:

                if "dateTime" not in event.get(
                    "start",
                    {}
                ):
                    continue

                # Si hay un evento que no es el que estamos excluyendo, está ocupado
                if exclude_event_id and event.get("id") == exclude_event_id:
                    continue

                return False

            return True

        except HttpError:

            raise

    def create_event(
        self,
        calendar_id: str,
        title: str,
        start_datetime: datetime,
        end_datetime: datetime,
    ):

        start_datetime = (
            self._ensure_chile_timezone(
                start_datetime
            )
        )

        end_datetime = (
            self._ensure_chile_timezone(
                end_datetime
            )
        )

        service = (
            self._get_calendar_service()
        )

        event = {
            "summary": title,
            "start": {
                "dateTime":
                    start_datetime.isoformat(),
                "timeZone":
                    CHILE_TIMEZONE,
            },
            "end": {
                "dateTime":
                    end_datetime.isoformat(),
                "timeZone":
                    CHILE_TIMEZONE,
            },
        }

        try:

            return (
                service.events()
                .insert(
                    calendarId=calendar_id,
                    body=event,
                )
                .execute()
            )

        except HttpError:

            raise

    def delete_event(
        self,
        calendar_id: str,
        event_id: str,
    ):

        service = (
            self._get_calendar_service()
        )

        try:

            (
                service.events()
                .delete(
                    calendarId=calendar_id,
                    eventId=event_id,
                )
                .execute()
            )

            return True

        except HttpError:

            raise

    def update_event(
        self,
        calendar_id: str,
        event_id: str,
        start_datetime: datetime,
        end_datetime: datetime,
    ):

        start_datetime = (
            self._ensure_chile_timezone(
                start_datetime
            )
        )

        end_datetime = (
            self._ensure_chile_timezone(
                end_datetime
            )
        )

        service = (
            self._get_calendar_service()
        )

        try:

            event = (
                service.events()
                .get(
                    calendarId=calendar_id,
                    eventId=event_id,
                )
                .execute()
            )

            event["start"] = {
                "dateTime":
                    start_datetime.isoformat(),
                "timeZone":
                    CHILE_TIMEZONE,
            }

            event["end"] = {
                "dateTime":
                    end_datetime.isoformat(),
                "timeZone":
                    CHILE_TIMEZONE,
            }

            return (
                service.events()
                .update(
                    calendarId=calendar_id,
                    eventId=event_id,
                    body=event,
                )
                .execute()
            )

        except HttpError:

            raise