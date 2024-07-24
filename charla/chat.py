import argparse
import re
from collections.abc import Mapping
from datetime import datetime
from operator import itemgetter
from pathlib import Path

import httpx
import ollama
from html2text import html2text
from prompt_toolkit import HTML, PromptSession
from prompt_toolkit import print_formatted_text as print_fmt
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import PathCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding import KeyBindings

from charla import config

# UI text

t_open = 'OPEN: '
t_open_toolbar = 'Add to prompt: '
t_prompt = 'PROMPT: '
t_prompt_ml = 'PROMPT \N{LATIN SUBSCRIPT SMALL LETTER M}\N{LATIN SUBSCRIPT SMALL LETTER L}: '
t_response = 'RESPONSE:'
t_help = '''
Press CTRL-C or CTRL-D to exit chat.
Press RETURN to send prompt in single line mode.
Press ALT+M to switch between single and multi line mode.
Press ALT+RETURN to send prompt in multi line mode.
Press CTRL-O to open a file or web page and append its content to the prompt.
Press CTRL-R or CTRL-S to search prompt history.
Press ↑ and ↓ to navigate previously entered prompts.
Press → to complete an auto suggested prompt.
'''


def available_models() -> None | list[str]:
    """Return available models sorted by size."""

    if model_list := ollama.list()['models']:
        return sorted(model_list, key=itemgetter('size'))
    return None


def generate(model: str, prompt: str, context: list, output: list, system=None) -> list:
    """Generate and print a response to the prompt and return the context."""

    stream = ollama.generate(model=model, prompt=prompt, context=context, stream=True, system=system)

    text = ''
    for chunk in stream:
        if not isinstance(chunk, Mapping):
            continue
        if not chunk['done']:
            text += chunk['response']
            print(chunk['response'], end='', flush=True)

    output.append(f'{t_response}\n\n{text}\n')
    return chunk['context'] if isinstance(chunk, Mapping) else []


def get_content(source: str) -> str:
    """Return content of the given source or empty string."""

    content = ''

    if source.startswith(('http://', 'https://')):
        try:
            resp = httpx.get(source, follow_redirects=True)
            content = html2text(
                resp.text, baseurl=source
            ) if resp.headers['content-type'] == 'text/html' else resp.text
        except httpx.ConnectError as err:
            print(f'Enter an existing URL.\n{err}\n')
    else:
        try:
            content = Path(source).read_text()
        except (FileNotFoundError, PermissionError) as err:
            print(f'Enter name of an existing file.\n{err}\n')

    return content


def prompt_session(argv: argparse.Namespace) -> PromptSession:
    """Create and return a PromptSession object."""

    session: PromptSession = PromptSession(message=t_prompt_ml if argv.multiline else t_prompt,
                            history=FileHistory(argv.prompt_history),
                            auto_suggest=AutoSuggestFromHistory(),
                            multiline=argv.multiline)

    print(t_help)

    bindings = KeyBindings()

    @bindings.add('escape', 'm')
    def switch_multiline(_event):
        session.multiline = not session.multiline
        session.message = t_prompt_ml if session.multiline else t_prompt

    @bindings.add('c-o')
    def fetch(_event):
        session.message = t_open
        session.completer = PathCompleter(only_directories=False, expanduser=True)

    session.key_bindings = bindings

    return session


def run(argv: argparse.Namespace) -> None:
    """Run the chat session."""

    context: list[int] = []  # Store conversation history to make the model context aware
    output = [f'# Chat with: {argv.model}\n']  # List to store output text

    history = Path(argv.prompt_history)
    config.mkdir(history.parent, exist_ok=True, parents=True)

    session = prompt_session(argv)
    print_fmt('Chat with:', HTML(f'<ansigreen>{argv.model}</ansigreen>'), '\n')

    system_prompt = argv.system_prompt.read() if argv.system_prompt else ''
    if system_prompt:
        print_fmt('Using system prompt:', HTML(f'<ansigreen>{argv.system_prompt.name}</ansigreen>'), '\n')

    open_source = ''

    while True:
        try:
            if not (user_input := session.prompt()):
                continue

            output.append(f'{session.message}{user_input}\n')

            if session.message == t_open:
                open_source = user_input.strip()
                session.bottom_toolbar = t_open_toolbar + open_source
                session.message = t_prompt_ml if session.multiline else t_prompt
                session.completer = None
                continue

            if open_source:
                if content := get_content(open_source):
                    user_input = user_input.strip() + '\n\n' + content
                else:
                    continue

            print(f'\n{t_response}\n')
            context = generate(argv.model, user_input, context, output, system=system_prompt)
            print('\n')

            system_prompt = ''
            session.bottom_toolbar = None

        # Exit program on CTRL-C and CTRL-D
        except (KeyboardInterrupt, EOFError):
            break

    chats_path = Path(argv.chats_path)
    config.mkdir(chats_path, exist_ok=True, parents=True)
    save(chats_path, output, argv.model)
    print_fmt(HTML('<b>Exiting program.</b>'))


def save(chats_path: Path, output: list[str], model_name: str) -> None:
    """Save the chat as a markdown file."""

    if len(output) > 1:
        now = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
        slug = re.sub(r'\W', '-', model_name)
        file = chats_path / f'{now}-{slug}.md'

        print(f'Saving chat in: {file}')
        file.write_text('\n'.join(output))
