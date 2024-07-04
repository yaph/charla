import argparse
import re
import sys
from datetime import datetime
from operator import itemgetter
from pathlib import Path
from typing import Mapping

import ollama
from prompt_toolkit import HTML, PromptSession
from prompt_toolkit import print_formatted_text as print_fmt
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding import KeyBindings

from charla import config


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
        if not isinstance(chunk, Mapping):
            continue
        if not chunk['done']:
            text += chunk['response']
            print(chunk['response'], end='', flush=True)

    output.append(f'{t_response}\n\n{text}\n')
    return chunk['context'] if isinstance(chunk, Mapping) else []


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


def run(argv: argparse.Namespace) -> None:
    context: list[int] = []  # Store conversation history to make the model context aware
    output = [f'# Chat with: {argv.model}\n']  # List to store output text

    history = Path(argv.prompt_history)
    config.mkdir(history.parent, exist_ok=True, parents=True)
    session = prompt_session(history)
    print_fmt('Chat with:', HTML(f'<ansigreen>{argv.model}</ansigreen>'), '\n')

    while True:
        try:
            user_input = session.prompt()
            if not user_input:
                continue

            output.append(f'{t_prompt}{user_input}\n')
            print(f'\n{t_response}\n')
            context = generate(argv.model, user_input, context, output)
            print('\n')
        # Exit program on CTRL-C and CTRL-D
        except (KeyboardInterrupt, EOFError):
            break

    chats_path = Path(argv.chats_path)
    config.mkdir(chats_path, exist_ok=True, parents=True)
    save(chats_path, output, argv.model)

    print_fmt(HTML('<b>Exiting program.</b>'))
    sys.exit()


def save(chats_path: Path, output: list[str], model_name: str) -> None:
    if len(output) > 1:
        now = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
        slug = re.sub(r'\W', '-', model_name)
        file = chats_path / f'{now}-{slug}.md'

        print(f'Saving chat in: {file}')
        file.write_text('\n'.join(output))
