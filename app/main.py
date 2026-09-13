import os
import logging
from fastapi import FastAPI
from app.api import router
from app.database import Base, engine
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/mdu.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Crear tablas
Base.metadata.create_all(bind=engine)

# Determinar el entorno de ejecución
ENV = os.getenv("ENV", "").lower()
IS_PRODUCTION = ENV == "production"

# Crear aplicación FastAPI
# En producción deshabilitamos la documentación interactiva.
app = FastAPI(
    title="MDU - Motor de Disponibilidad Universal",
    description="API para gestión de disponibilidad y reservas",
    version="1.0.0",
    docs_url=None if IS_PRODUCTION else "/docs",
    redoc_url=None if IS_PRODUCTION else "/redoc",
    openapi_url=None if IS_PRODUCTION else "/openapi.json",
)

# Registrar rutas
app.include_router(router)

logger.info("Servidor MDU iniciado correctamente")
logger.info(f"Base de datos: {os.getenv('DATABASE_URL', 'sqlite:///./bookings.db')}")