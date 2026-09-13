import os

from dotenv import load_dotenv
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

# Cargar variables de entorno
load_dotenv()

API_KEY_NAME = "X-API-Key"
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise RuntimeError(
        "La variable de entorno API_KEY no está definida. "
        "Configúrala (por ejemplo en tu archivo .env) antes de arrancar el servidor."
    )

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header)):
    """
    Verifica que la API Key sea válida.
    """
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key inválida o ausente.",
        )
    return api_key