from typing import TypedDict


class AIResponse(TypedDict):

    intent: str

    customer_name: str | None

    service_name: str | None

    resource_name: str | None

    date: str | None

    time: str | None

    booking_id: str | None

    message: str


def interpret_message(
    message: str,
) -> AIResponse:
    """
    Interpreta un mensaje del usuario.

    Por ahora es un stub.
    Más adelante utilizará OpenAI,
    Gemini o cualquier otro modelo.
    """

    return {

        "intent": "unknown",

        "customer_name": None,

        "service_name": None,

        "resource_name": None,

        "date": None,

        "time": None,

        "booking_id": None,

        "message": message,
    }