from abc import ABC, abstractmethod


class AIProvider(ABC):
    """
    Interfaz base para cualquier proveedor de IA.
    """

    @abstractmethod
    def chat(
        self,
        system_prompt: str,
        user_message: str,
    ) -> str:
        pass