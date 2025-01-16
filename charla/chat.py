import argparse
import re
from datetime import datetime
from pathlib import Path

import httpx
from html2text import html2text
from prompt_toolkit import HTML, PromptSession
from prompt_toolkit import print_formatted_text as print_fmt
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import PathCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding import KeyBindings

from charla import client, config, ui


def get_content(location: str) -> str:
    """Return content of the given source or empty string.

    Args:
        location (str): The URL or file path to fetch content from.
    """

    content = ''

    if location.startswith(('http://', 'https://')):
        try:
            resp = httpx.get(location, follow_redirects=True)
            content = (
                html2text(resp.text, baseurl=location) if resp.headers['content-type'] == 'text/html' else resp.text
            )
        except httpx.ConnectError as err:
            print(f'Enter an existing URL.\n{err}\n')
    else:
        try:
            content = Path(location).expanduser().read_text()
        except (FileNotFoundError, PermissionError) as err:
            print(f'Enter name of an existing file.\n{err}\n')

    return content


def prompt_session(argv: argparse.Namespace) -> PromptSession:
    """Create and return a PromptSession object."""

    session: PromptSession = PromptSession(
        message=ui.t_prompt_ml if argv.multiline else ui.t_prompt,
        history=FileHistory(argv.prompt_history),
        auto_suggest=AutoSuggestFromHistory(),
        multiline=argv.multiline,
    )

    print(ui.t_help)

    bindings = KeyBindings()

    @bindings.add('escape', 'm')
    def switch_multiline(_event):
        session.multiline = not session.multiline
        session.message = ui.t_prompt_ml if session.multiline else ui.t_prompt

    @bindings.add('c-o')
    def fetch(_event):
        session.message = ui.t_open
        session.completer = PathCompleter(only_directories=False, expanduser=True)

    session.key_bindings = bindings

    return session


def run(argv: argparse.Namespace) -> None:
    """Run the chat session."""

    # File name or URL to be opened.
    open_location = ''

    # Prompt used to give directions to the model at the beginning of the chat.
    system_prompt = Path(argv.system_prompt).read_text() if argv.system_prompt else ''

    # Determine which Client class to import.
    if argv.provider == 'ollama':
        from charla.client.ollama import OllamaClient as ApiClient
    elif argv.provider == 'github':
        from charla.client.github import AzureClient as ApiClient  # type: ignore

    # Start model API client before chat REPL in case of model errors.
    client = ApiClient(argv.model, system=system_prompt, message_limit=argv.message_limit)
    client.set_info()

    # Prompt history used for auto completion.
    history = Path(argv.prompt_history)
    config.mkdir(history.parent, exist_ok=True, parents=True)

    # Location to store chat as markdown file.
    chats_path = Path(argv.chats_path)
    config.mkdir(chats_path, exist_ok=True, parents=True)
    now = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
    slug = re.sub(r'\W', '-', client.model)
    chat_file = chats_path / f'{now}-{slug}.md'

    # Start the chat REPL.
    session = prompt_session(argv)
    print_fmt('Chat with:', HTML(f'<ansigreen>{argv.model}</ansigreen>'), '\n')
    if system_prompt:
        print_fmt('Using system prompt:', HTML(f'<ansigreen>{argv.system_prompt}</ansigreen>'), '\n')

    while True:
        try:
            if not (user_input := session.prompt()):
                continue

            # Handle OPEN command input and continue to next prompt.
            if session.message == ui.t_open:
                open_location = user_input.strip()
                session.bottom_toolbar = ui.t_open_toolbar + open_location
                session.message = ui.t_prompt_ml if session.multiline else ui.t_prompt
                session.completer = None
                continue

            # Read content from location and append it to user message.
            if open_location:
                if content := get_content(open_location):
                    user_input = user_input.strip() + '\n\n' + content
                    open_location = ''
                    session.bottom_toolbar = None
                else:
                    continue

            print(f'\n{ui.t_response}\n')
            client.generate(user_input)
            print('\n')

            save(chat_file, client)

        # Exit program on CTRL-C and CTRL-D
        except (KeyboardInterrupt, EOFError):
            break

    # Save chat if there is at least one response.
    if any(m['role'] == 'assistant' for m in client.message_history):
        print(f'Saving chat in: {chat_file}')
        save(chat_file, client)

    print_fmt(HTML('<b>Exiting program.</b>'))


def save(chat_file: Path, client: client.Client) -> None:
    """Save the chat as a markdown file."""

    output = f'# Chat with: {client.model}\n\n'

    # Add user and assistant messages to output.
    for msg in client.message_history:
        if msg['role'] == 'user':
            output += f"{ui.t_prompt}{msg['text']}\n\n"
        elif msg['role'] == 'assistant':
            output += f"{ui.t_response}\n\n{msg['text']}\n\n"

    chat_file.write_text(output)
