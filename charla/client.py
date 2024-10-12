import os
import sys
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
        try:
            response = self.client.generate(model=self.model, prompt=prompt, context=self.context, system=self.system)
        except Exception as err:
            print(f'Error: {err}')
            return

        # Make sure system message is set only once.
        self.system = ''

        text = response['response'] # type: ignore
        print(text)

        self.context = response['context'] # type: ignore
        self.output.append(ui.response(text))

        # FIXME make sure context doesn't get too big.
        # Check len(self.context)


class AzureClient(Client):
    def __init__(self, model: str, context: list[str], output: list[str], system: str = ''):
        super().__init__(model, context, output, system)

        if not (token := os.getenv('GITHUB_TOKEN')):
            sys.exit('GITHUB_TOKEN environment variable is not set or empty.')

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

        try:
            response = self.client.complete(messages=self.context)
        except Exception as err:
            print(f'Error: {err}')
            return

        text = response.choices[0].message.content
        print(text)

        self.context.append(AssistantMessage(content=text))
        self.output.append(ui.response(text))

        # FIXME make sure context doesn't get too big.
        # Check response.usage
