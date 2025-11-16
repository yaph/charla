from abc import ABC, abstractmethod
from collections import deque
from typing import Any, Literal, NamedTuple


class ModelInfo(NamedTuple):
    architecture: str
    context_length: int


class Client(ABC):

    provider: str

    def __init__(self, model: str, system: str = '', **kwargs):
        self.model = model
        self.system = system

        # For saving chat.
        self.message_history: list[dict] = []

        # For chatting with memory.
        self.context: Any = deque([], maxlen=kwargs.get('message_limit'))

        # For enabling thinking mode.
        self.think: Literal['low', 'medium', 'high'] | bool | None = kwargs.get('think')

    @abstractmethod
    def add_context(self, *, role: str, text: str):
        pass

    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass

    def add_message(self, *, role: str, text: str):
        self.message_history.append({'role': role, 'text': text})
        self.add_context(role=role, text=text)

    def set_info(self):
        pass
