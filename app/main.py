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
        logging.FileHandler("mdu.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Crear tablas
Base.metadata.create_all(bind=engine)

# Crear aplicación FastAPI
app = FastAPI(
    title="MDU - Motor de Disponibilidad Universal",
    description="API para gestión de disponibilidad y reservas",
    version="1.0.0",
)

# Registrar rutas
app.include_router(router)

logger.info("Servidor MDU iniciado correctamente")
logger.info(f"Base de datos: {os.getenv('DATABASE_URL', 'sqlite:///./bookings.db')}")