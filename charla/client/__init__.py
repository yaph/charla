from abc import ABC, abstractmethod
from collections import deque
from typing import Any, Literal, NamedTuple


class ClientError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class ModelInfo(NamedTuple):
    architecture: str
    context_length: int


class Client(ABC):
    provider: str | None = None

    def __init_subclass__(cls, **kwargs):
        """Enforce non-empty provider attribute in subclasses."""
        super().__init_subclass__(**kwargs)
        if not getattr(cls, 'provider', None):
            msg = f'{cls.__name__} must set a non-empty "provider" class attribute'
            raise TypeError(msg)

    def __init__(self, model: str, **kwargs):
        self.model = model
        self.system = kwargs.get('system')

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
