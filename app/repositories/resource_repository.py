from fastapi import HTTPException

from app.datasource.memory_datasource import RESOURCES
from app.models import Resource


def get_resource(
    resource_id: int,
) -> Resource:
    """
    Obtiene un recurso por su identificador.
    """

    resource = RESOURCES.get(resource_id)

    if resource is None:

        raise HTTPException(
            status_code=404,
            detail="Recurso no encontrado.",
        )

    return resource