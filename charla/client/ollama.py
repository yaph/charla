import sys

import ollama

from charla.client import Client, ClientError, ModelInfo


class OllamaClient(Client):
    provider: str = 'ollama'

    def __init__(self, model: str, **kwargs):
        super().__init__(model, **kwargs)
        self.client = ollama.Client()

        if system := kwargs.get('system'):
            self.add_message(role='system', text=system)

    def add_context(self, *, role: str, text: str):
        self.context.append({'role': role, 'content': text})

    def set_info(self):
        """Request model info from API and set model_info property."""

        # Make sure model exists or exit program.
        try:
            info = self.client.show(self.model)
        except ollama.ResponseError as err:
            sys.exit(f'Error: {err}')

        # Save model context length in meta property, that can be expanded if useful.
        arch = info.modelinfo['general.architecture']
        self.model_info = ModelInfo(architecture=arch, context_length=int(info.modelinfo[f'{arch}.context_length']))

    def generate(self, prompt: str) -> str:
        self.add_message(role='user', text=prompt)
        response = self.client.chat(model=self.model, messages=self.context, think=self.think)

        try:
            text = response.message.content or ''
        except ollama.ResponseError as err:
            raise ClientError(err) from err

        self.add_message(role='assistant', text=text)
        return text.strip()
