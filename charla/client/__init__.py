from abc import ABC, abstractmethod
from collections import deque
from typing import Any, NamedTuple


class ModelInfo(NamedTuple):
    architecture: str
    context_length: int


class Client(ABC):
    def __init__(self, model: str, system: str = '', **kwargs):
        self.model = model
        self.system = system

        # For saving chat.
        self.message_history: list[dict] = []

        # For chatting with memory.
        self.message_length: int | None = kwargs.get('message_length')
        self.context: Any = deque([], maxlen=kwargs.get('message_limit'))

    @abstractmethod
    def generate(self, prompt: str):
        pass

    def set_info(self):
        pass

    def add_message(self, role, text):
        self.message_history.append({'role': role, 'text': text})
