from app.providers.ai.openai_provider import interpret_message
import os

print(os.getenv("OPENAI_API_KEY"))

respuesta = interpret_message(
    "Hola, quiero una consulta mañana a las 10"
)

print(respuesta)