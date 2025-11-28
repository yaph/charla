import os
import sys
from typing import Any

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import AssistantMessage, SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import (
    ClientAuthenticationError,
    HttpResponseError,
    ServiceRequestError,
    ServiceResponseError,
)

from charla.client import Client, ClientError


class GithubClient(Client):
    provider: str = 'github'

    def __init__(self, model: str, **kwargs):
        super().__init__(model, **kwargs)

        if not (token := os.getenv('GITHUB_TOKEN')):
            sys.exit('GITHUB_TOKEN environment variable is not set or empty.')

        self.client = ChatCompletionsClient(
            endpoint='https://models.inference.ai.azure.com', credential=AzureKeyCredential(token), model=model
        )

        if system := kwargs.get('system'):
            self.add_message(role='system', text=system)

    def __del__(self):
        self.client.close()

    def add_context(self, *, role: str, text: str):
        context: Any = None
        match role:
            case 'system':
                context = SystemMessage(content=text)
            case 'user':
                context = UserMessage(content=text)
            case 'assistant':
                context = AssistantMessage(content=text)
        self.context.append(context)

    def generate(self, prompt: str) -> str:
        self.add_message(role='user', text=prompt)

        try:
            response = self.client.complete(messages=list(self.context))
        except ClientAuthenticationError as err:
            sys.exit(f'Error: {err}')
        except (HttpResponseError, ServiceRequestError, ServiceResponseError) as err:
            raise ClientError(err)

        try:
            text = response['choices'][0].message.content
            self.add_message(role='assistant', text=text)
        except UnicodeDecodeError as err:
            raise ClientError(err)

        return text.strip()
