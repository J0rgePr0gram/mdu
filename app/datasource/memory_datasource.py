from app.models import (
    Resource,
    Calendar,
    Service,
)


# ============================================================
# RECURSOS
# ============================================================

RESOURCES = {

    1: Resource(
        id=1,
        name="Dr. Martinez",
        resource_type="person",
        calendar_id=1,
    ),

}

# ============================================================
# CALENDARIOS
# ============================================================

CALENDARS = {

    1: Calendar(
        id=1,
        provider="google",
        external_id="d41237753a7ca205074652e46271a711d385d2b18ac66d0f6c6adcaa77047fbf@group.calendar.google.com",
    ),

}


# ============================================================
# SERVICIOS
# ============================================================

SERVICES = {

    "Consulta": Service(
        id=1,
        name="Consulta",
        duration=45,
    ),

}