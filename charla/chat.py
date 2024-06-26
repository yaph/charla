from datetime import datetime
from operator import itemgetter
from pathlib import Path
from typing import Any, Union

from platformdirs import user_cache_path, user_documents_path
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding import KeyBindings

import re

import ollama


chat_history = user_documents_path() / 'charla' / 'chats'
chat_history.mkdir(exist_ok=True, parents=True)
prompt_history = user_cache_path(appname='charla', ensure_exists=True) / 'prompt-history.txt'

# UI text
t_prompt = 'PROMPT: '
t_prompt_ml = 'PROMPT \N{LATIN SUBSCRIPT SMALL LETTER M}\N{LATIN SUBSCRIPT SMALL LETTER L}: '
t_response = 'RESPONSE:'
t_help = '''
Press CTRL-C or CTRL-D to exit chat.
Press ALT+M to switch between single and multi line mode.
Press ALT+RETURN to send prompt in multi line mode.
Press ↑ and ↓ to navigate previously entered prompts.
Press → to complete an auto suggested prompt.
'''

def available_models() -> Union[None, list[str]]:
    """Return available models sorted by size."""

    if model_list := ollama.list()['models']:
        return [m for m in sorted(model_list, key=itemgetter('size'))]


def generate(model: str, prompt: str, context: list, output: list) -> str | Any:
    stream = ollama.generate(model=model, prompt=prompt, context=context, stream=True)

    text = ''
    for chunk in stream:
        if not chunk['done']:
            text += chunk['response']
            print(chunk['response'], end='', flush=True)

    output.append(f'{t_response}\n\n{text}\n')
    return chunk['context']


def prompt_session() -> PromptSession:
    session = PromptSession(message=t_prompt,
                            history=FileHistory(prompt_history),
                            auto_suggest=AutoSuggestFromHistory())

    print(t_help)

    bindings = KeyBindings()

    @bindings.add('escape', 'm')
    def switch_multiline(event):
        session.multiline = not session.multiline
        session.message = t_prompt if session.multiline is False else t_prompt_ml

    session.key_bindings = bindings

    return session


def save(output: list[str], model_name: str) -> None:
    if len(output) > 1:
        now = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
        slug = re.sub(r'\W', '-', model_name)
        file = chat_history / f'{now}-{slug}.md'
        print(f'Saving chat in: {file}')
        file.write_text('\n'.join(output))
