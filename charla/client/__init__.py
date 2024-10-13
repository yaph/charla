from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, NamedTuple


class ModelInfo(NamedTuple):
    architecture: str
    context_length: int


@dataclass
class Client(ABC):
    model: str
    context: Any
    output: list[str]
    system: str = ''

    @abstractmethod
    def generate(self, prompt: str):
        pass
