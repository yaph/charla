import re
from datetime import datetime
from operator import itemgetter
from pathlib import Path
from typing import Any

import ollama
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding import KeyBindings

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

def available_models() -> None | list[str]:
    """Return available models sorted by size."""

    if model_list := ollama.list()['models']:
        return sorted(model_list, key=itemgetter('size'))
    return None


def generate(model: str, prompt: str, context: list, output: list) -> list:
    stream = ollama.generate(model=model, prompt=prompt, context=context, stream=True)

    text = ''
    for chunk in stream:
        if not isinstance(chunk, dict):
            continue
        if not chunk['done']:
            text += chunk['response']
            print(chunk['response'], end='', flush=True)

    output.append(f'{t_response}\n\n{text}\n')
    return chunk['context'] if isinstance(chunk, dict) else []


def prompt_session(history: Path) -> PromptSession:
    session: PromptSession = PromptSession(message=t_prompt,
                            history=FileHistory(history),
                            auto_suggest=AutoSuggestFromHistory())

    print(t_help)

    bindings = KeyBindings()

    @bindings.add('escape', 'm')
    def switch_multiline(_event):
        session.multiline = not session.multiline
        session.message = t_prompt if session.multiline is False else t_prompt_ml

    session.key_bindings = bindings

    return session


def save(chats_path: Path, output: list[str], model_name: str) -> None:
    if len(output) > 1:
        now = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
        slug = re.sub(r'\W', '-', model_name)
        file = chats_path / f'{now}-{slug}.md'

        print(f'Saving chat in: {file}')
        file.write_text('\n'.join(output))
