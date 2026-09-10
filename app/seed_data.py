import sys
import uuid
from pathlib import Path

# Asegura que el directorio raíz del proyecto esté en sys.path para que
# los imports del paquete 'app' funcionen cuando se ejecuta directamente
# (ej: python app/seed_data.py dentro del contenedor Docker).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import Base, SessionLocal, engine
from app.models_db import ResourceDB, ServiceDB, CalendarDB

def seed_database():
    # Crear tablas si no existen (cuando se ejecuta standalone)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    
    # Crear un recurso de prueba (merge para que sea idempotente)
    resource = ResourceDB(
        id=1,
        name="Dr. Martinez",
        resource_type="professional"
    )
    db.merge(resource)
    
    # Crear un servicio de prueba (merge para que sea idempotente)
    service = ServiceDB(
        id=1,
        name="Consulta",
        duration=45
    )
    db.merge(service)
    
    # Crear un calendario de prueba (merge para que sea idempotente)
    calendar = CalendarDB(
        id=1,
        resource_id=1,
        provider="mock",
        external_id="mock_calendar_1"
    )
    db.merge(calendar)
    
    db.commit()
    db.close()
    print("✅ Datos de prueba sembrados correctamente")

if __name__ == "__main__":
    seed_database()