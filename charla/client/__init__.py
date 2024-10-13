from abc import ABC, abstractmethod
from collections import namedtuple

from dataclasses import dataclass
from typing import Any


ModelInfo = namedtuple('ModelInfo', 'architecture context_length')


@dataclass
class Client(ABC):
    model: str
    context: Any
    output: list[str]
    system: str = ''

    @abstractmethod
    def generate(self, prompt: str):
        pass
