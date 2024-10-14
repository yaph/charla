import os
import sys

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import AssistantMessage, SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import ClientAuthenticationError, HttpResponseError

from charla.client import Client


class AzureClient(Client):
    def __init__(self, model: str, system: str = ''):
        super().__init__(model, system)

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
            self.add_message(role='system', text=system)


    def __del__(self):
        self.client.close()


    def generate(self, prompt: str):
        self.context.append(UserMessage(content=prompt))
        self.add_message(role='user', text=prompt)

        # TODO: make sure context doesn't get too big.
        # Check sum of messages lengths.
        try:
            response = self.client.complete(messages=self.context, stream=True)
        except (ClientAuthenticationError, HttpResponseError) as err:
            sys.exit(f'Error: {err}')

        text = ''
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                text += content
                print(content, end='', flush=True)

        self.context.append(AssistantMessage(content=text))
        self.add_message(role='assistant', text=text)

