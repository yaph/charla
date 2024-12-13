import sys

import ollama

from charla.client import Client, ModelInfo


class OllamaClient(Client):
    def __init__(self, model: str, system: str = '', **kwargs):
        super().__init__(model, system, **kwargs)

        # For chatting with memory.
        self.context: list[int] = []

        self.client = ollama.Client()

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

    def generate(self, prompt: str):
        self.add_message(role='user', text=prompt)
        response = self.client.generate(
            model=self.model, prompt=prompt, context=self.context, stream=True, system=self.system
        )

        # Make sure system message is set only once.
        self.system = ''

        text = ''
        try:
            for chunk in response:
                if not chunk['done']:
                    content = chunk['response']
                    if content:
                        text += content
                        print(content, end='', flush=True)
        except ollama.ResponseError as err:
            sys.exit(f'Error: {err}')

        self.context = chunk['context']
        self.add_message(role='assistant', text=text)
