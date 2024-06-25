from pathlib import Path
from datetime import datetime
from operator import itemgetter
from typing import Union

from platformdirs import user_config_dir
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding import KeyBindings

import ollama


config_dir = user_config_dir(appname='charla', ensure_exists=True)
context_length = 4096  # TODO: Derive this from model data when available

p_history = Path(config_dir) / 'prompt-history.txt'

# UI text
t_prompt = 'PROMPT: '
t_prompt_ml = 'PROMPT \N{LATIN SUBSCRIPT SMALL LETTER M}\N{LATIN SUBSCRIPT SMALL LETTER L}: '
t_response = 'RESPONSE:'
t_help = '''Press CTRL-C or CTRL-D to exit.
Press ALT+M to switch between single and multi line mode.
Press ALT+RETURN to send prompt in multi line mode.
'''

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

    output.append(f'{t_response}\n{text}\n')
    return chunk['context']


def get_session() -> PromptSession:
    session = PromptSession(message=t_prompt, history=FileHistory(p_history))
    print(t_help)

    bindings = KeyBindings()

    @bindings.add('escape', 'm')
    def switch_multiline(event):
        session.multiline = not session.multiline
        session.message = t_prompt if session.multiline is False else t_prompt_ml

    session.key_bindings = bindings

    return session


def save_chat(output: list[str]) -> None:
    if output:
        now = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
        Path(f'chat-history-{now}.txt').write_text('\n'.join(output))


