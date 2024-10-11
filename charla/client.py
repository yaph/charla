import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

import ollama
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential

import charla.ui as ui


@dataclass
class Client(ABC):
    model: str
    context: Any
    output: list[str]
    system: str = ''

    @abstractmethod
    def generate(self, prompt: str):
        pass


class OllamaClient(Client):
    def __init__(self, model: str, context: list[int], output: list[str], system: str = ''):
        super().__init__(model, context, output, system)

        self.client = ollama.Client()


    def generate(self, prompt: str):
        response = self.client.generate(model=self.model, prompt=prompt, context=self.context, system=self.system)

        # Make sure system message is set only once.
        self.system = ''

        text = response['response'] # type: ignore
        print(text)

        self.context = response['context'] # type: ignore
        self.output.append(ui.response(text))


class AzureClient(Client):
    def __init__(self, model: str, context: list[str], output: list[str], system: str = ''):
        super().__init__(model, context, output, system)

        token = os.environ['GITHUB_TOKEN']
        endpoint = 'https://models.inference.ai.azure.com'

        self.client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(token),
            model=model
        )

        if system:
            self.context.append(SystemMessage(content=system))


    def generate(self, prompt: str):
        self.context.append(UserMessage(content=prompt))

        response = self.client.complete(messages=self.context)
        text = response.choices[0].message.content
        print(text)

        self.context.append(AssistantMessage(content=text))
        self.output.append(ui.response(text))
