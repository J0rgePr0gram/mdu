# MDU - Motor de Disponibilidad Universal

**Backend de reservas agnóstico al recurso y al proveedor de calendario, construido con Python, FastAPI y Google Calendar.**

[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.139-green)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-29.7-blue)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/tests-18%20passed-brightgreen)]()

---

## 📋 Descripción

El **Motor de Disponibilidad Universal (MDU)** es un backend de reservas diseñado para ser:

- **Agnóstico al tipo de recurso**: profesionales, salas, vehículos, equipos, etc.
- **Agnóstico al proveedor de calendario**: Google Calendar, Outlook, iCloud o cualquier otro.
- **Reutilizable**: la misma lógica funciona para clínicas, gimnasios, profesionales independientes, talleres y más.

El MDU responde a la pregunta universal: **"¿Cuándo puede reservarse este recurso para este servicio?"** y gobierna todo el ciclo de vida de la reserva.

---

## ✨ Características

- ✅ **API REST completa** con documentación automática (Swagger/OpenAPI).
- ✅ **Integración con Google Calendar** (crear, leer, actualizar, eliminar eventos).
- ✅ **Persistencia en SQLite** con SQLAlchemy.
- ✅ **UUID como identificador universal** para reservas.
- ✅ **Manejo de estados** (active/cancelled).
- ✅ **Consistencia transaccional** entre Google Calendar y SQLite.
- ✅ **Proveedores intercambiables** (GoogleCalendarProvider, MockCalendarProvider).
- ✅ **Suite de 18 tests automatizados** con pytest.
- ✅ **Desplegable con Docker** (Dockerfile + docker-compose.yml).
- ✅ **Logging profesional** en archivo y consola.

---

## 🏗️ Arquitectura
┌─────────────────────────────────────────────────────────┐
│ CLIENTES / CANALES │
│ (Web, WhatsApp, Instagram, Email, etc.) │
└────────────────────────┬────────────────────────────────┘
│ HTTP/REST
▼
┌─────────────────────────────────────────────────────────┐
│ API (FastAPI) │
│ Endpoints REST + Swagger │
└────────────────────────┬────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────┐
│ SERVICIOS DE NEGOCIO │
│ booking_service · cancellation_service · reschedule │
│ availability_service │
└────────────┬───────────────────────────┬────────────────┘
│ │
▼ ▼
┌────────────────────────┐ ┌──────────────────────────┐
│ REPOSITORIOS │ │ PROVEEDORES │
│ (SQLAlchemy + SQLite) │ │ (CalendarProvider) │
│ │ │ │
│ - booking_repository │ │ - GoogleCalendarProvider│
│ - resource_repository │ │ - MockCalendarProvider │
│ - service_repository │ │ │
│ - calendar_repository │ │ │
└────────────────────────┘ └──────────────────────────┘
**Patrón de dependencias:** `API → Servicios → Repositorios/Proveedores`

---

## 🛠️ Tecnologías

| Componente | Tecnología |
|------------|------------|
| **Lenguaje** | Python 3.13 |
| **Framework Web** | FastAPI |
| **Base de Datos** | SQLite + SQLAlchemy 2.0 |
| **Calendario** | Google Calendar API v3 |
| **Autenticación** | OAuth 2.0 |
| **Contenedores** | Docker + Docker Compose |
| **Tests** | pytest + TestClient |
| **Logging** | Python logging |

---

## 🚀 Instalación

### Opción 1: Local (Python)

```bash
# 1. Clonar el repositorio
git clone https://github.com/J0rgePr0gram/mdu.git
cd mdu

# 2. Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
# Crea un archivo .env con:
# GOOGLE_CLIENT_ID=tu_client_id
# GOOGLE_CLIENT_SECRET=tu_client_secret
# GOOGLE_REDIRECT_URI=http://localhost:8000/callback
# DATABASE_URL=sqlite:///./data/bookings.db
# LOG_LEVEL=INFO

# 5. Agregar credentials.json (Google Cloud Console)

# 6. Ejecutar
uvicorn app.main:app --reload