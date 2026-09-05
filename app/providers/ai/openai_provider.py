import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from app.prompts.system_prompt import (
    BOOKING_ASSISTANT_PROMPT,
)

load_dotenv()

client = OpenAI(
    api_key=os.getenv(
        "OPENAI_API_KEY"
    )
)

def interpret_message(
    message: str,
) -> dict:
    """
    Envía un mensaje al LLM y devuelve
    el JSON interpretado.
    """

    response = client.chat.completions.create(

        model="gpt-5",

        messages=[

            {
                "role": "system",
                "content": BOOKING_ASSISTANT_PROMPT,
            },

            {
                "role": "user",
                "content": message,
            },

        ],

        temperature=0,

        response_format={
            "type": "json_object",
        },

    )

    content = (
        response
        .choices[0]
        .message
        .content
    )

    return json.loads(
        content
    )