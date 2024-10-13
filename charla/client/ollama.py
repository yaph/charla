import sys
import ollama
from collections.abc import Mapping

import charla.ui as ui
from charla.client import Client, ModelInfo


class OllamaClient(Client):
    def __init__(self, model: str, context: list[int], output: list[str], system: str = ''):
        super().__init__(model, context, output, system)

        self.client = ollama.Client()
        self._set_info()


    def _set_info(self):
        """Request model info from API and set model_info property."""

        # Make sure model exists or exit program.
        try:
            info = self.client.show(self.model)
        except Exception as err:
            sys.exit(f'Error: {err}')

        # Save model context length in meta property, that can be expanded if useful.
        arch = info['model_info']['general.architecture']
        self.model_info = ModelInfo(
            architecture=arch,
            context_length=int(info['model_info'][f'{arch}.context_length'])
        )


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
        # Check len(self.context) and meta info
