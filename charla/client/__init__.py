from abc import ABC, abstractmethod
from typing import Any, NamedTuple


class ModelInfo(NamedTuple):
    architecture: str
    context_length: int


class Client(ABC):
    def __init__(self, model: str, system: str = ''):
        self.model = model
        self.system = system
        # For chatting with memory and writing output.
        self.context: Any = []
        self.message_history: list[dict] = []

    @abstractmethod
    def generate(self, prompt: str):
        pass

    def set_info(self):
        pass

    def add_message(self, role, text):
        self.message_history.append({'role': role, 'text': text})
