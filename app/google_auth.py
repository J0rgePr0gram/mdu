import os
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/calendar']

CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI')
CHILE_TIMEZONE = os.getenv('CHILE_TIMEZONE', 'America/Santiago')


def get_credentials():
    """
    Obtiene credenciales de Google Calendar desde token.json o flujo OAuth.
    """
    creds = None
    token_path = Path('token.json')
    credentials_path = Path('credentials.json')

    # Cargar token si existe
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    # Si no hay credenciales válidas, iniciar flujo OAuth
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not credentials_path.exists():
                raise FileNotFoundError(
                    "No se encontró credentials.json. "
                    "Descárgalo desde Google Cloud Console."
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_path),
                SCOPES,
                redirect_uri=REDIRECT_URI
            )
            creds = flow.run_local_server(port=8000)

        # Guardar token para próximas ejecuciones
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return creds