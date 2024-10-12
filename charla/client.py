from collections.abc import Mapping
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
            response = self.client.generate(model=self.model, prompt=prompt, context=self.context, stream=True, system=self.system)
        except Exception as err:
            sys.exit(f'Error: {err}')

        # Make sure system message is set only once.
        self.system = ''

        text = ''
        for chunk in response:
            if not isinstance(chunk, Mapping):
                continue
            if not chunk['done']:
                content = chunk['response']
                if content:
                    text += content
                    print(content, end='', flush=True)

        if isinstance(chunk, Mapping):
            self.context = chunk['context']
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


    def __del__(self):
        self.client.close()


    def generate(self, prompt: str):
        self.context.append(UserMessage(content=prompt))

        try:
            response = self.client.complete(messages=self.context, stream=True)
        except Exception as err:
            sys.exit(f'Error: {err}')

        text = ''
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                text += content
                print(content, end='', flush=True)

        self.context.append(AssistantMessage(content=text))
        self.output.append(ui.response(text))

        # FIXME make sure context doesn't get too big.
        # Check response.usage
