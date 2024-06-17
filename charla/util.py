from pathlib import Path
from datetime import datetime
from operator import itemgetter
from typing import Union

from platformdirs import user_config_dir

import ollama


config_dir = user_config_dir(appname='charla', ensure_exists=True)
context_length = 4096  # TODO: Derive this from model data when available

# UI text
t_prompt = 'PROMPT: '
t_response = 'RESPONSE:'


def available_models() -> Union[None, list[str]]:
    """Return available models sorted by size."""

    if model_list := ollama.list()['models']:
        return [m for m in sorted(model_list, key=itemgetter('size'))]


def generate(model: str, prompt: str, context: list, output: list) -> list[int]:
    # Make sure the context doesn't get too long
    if len(context) > context_length:
        context = context[len(context)-context_length:]

    stream = ollama.generate(
        model=model,
        prompt=prompt,
        context=context,
        stream=True,
    )

    text = ''
    for chunk in stream:
        if not chunk['done']:
            text += chunk['response']
            print(chunk['response'], end='', flush=True)

    output.append(f'{t_response}\n\n{text}\n')
    return chunk['context']


def save_chat(output: list[str]) -> None:
    if output:
        now = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
        Path(f'chat-history-{now}.txt').write_text('\n'.join(output))