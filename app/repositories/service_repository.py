from fastapi import HTTPException

from app.datasource.memory_datasource import SERVICES
from app.models import Service


def get_service(
    service_name: str,
) -> Service:
    """
    Obtiene un servicio por su nombre.
    """

    service = SERVICES.get(service_name)

    if service is None:

        raise HTTPException(
            status_code=404,
            detail="Servicio no encontrado.",
        )

    return service