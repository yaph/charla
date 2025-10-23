import os
import sys

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import AssistantMessage, SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import ClientAuthenticationError, HttpResponseError

from charla.client import Client


class AzureClient(Client):
    def __init__(self, model: str, system: str = '', **kwargs):
        super().__init__(model, system, **kwargs)

        if not (token := os.getenv('GITHUB_TOKEN')):
            sys.exit('GITHUB_TOKEN environment variable is not set or empty.')

        self.client = ChatCompletionsClient(
            endpoint='https://models.inference.ai.azure.com', credential=AzureKeyCredential(token), model=model
        )

        if system:
            self.add_message(role='system', text=system)
            self.context.append(SystemMessage(content=system))

    def __del__(self):
        self.client.close()

    def generate(self, prompt: str):
        self.add_message(role='user', text=prompt)
        self.context.append(UserMessage(content=prompt))

        try:
            response = self.client.complete(messages=list(self.context), stream=True)
        except (ClientAuthenticationError, HttpResponseError) as err:
            sys.exit(f'Error: {err}')

        text = ''
        try:
            for chunk in response:
                if (choices := chunk.choices) and (content := choices[0].delta.content):
                    text += content
                    print(content, end='', flush=True)
        except UnicodeDecodeError:
            print('\nError: Received non-text response from the model.\n')
        else:
            self.add_message(role='assistant', text=text)
            self.context.append(AssistantMessage(content=text))
