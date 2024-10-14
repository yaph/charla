from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, NamedTuple


class ModelInfo(NamedTuple):
    architecture: str
    context_length: int


@dataclass
class Client(ABC):
    model: str
    context: Any = field(default_factory=list)
    message_history: list[dict] = field(default_factory=list)
    system: str = ''

    @abstractmethod
    def generate(self, prompt: str):
        pass

    def set_info(self):
        pass

    def add_message(self, role, text):
        self.message_history.append({'role': role, 'text': text})
