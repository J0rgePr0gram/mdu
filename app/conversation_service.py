from app.ai_interpreter import (
    interpret_message,
)


def process_message(
    message: str,
):
    """
    Punto de entrada de cualquier canal.

    WhatsApp,
    Instagram,
    Messenger,
    Telegram,
    Web Chat...
    """

    result = interpret_message(
        message
    )

    return result