#!/usr/bin/env python
import argparse
import sys
from pathlib import Path

from prompt_toolkit import HTML
from prompt_toolkit import print_formatted_text as print_fmt

from charla import chat, config


def main():
    if (models := chat.available_models()) is None:
        sys.exit('No language models available.')
    model_names = [m['name'] for m in models]

    user_settings = config.settings(config.load())
    user_settings['model'] = user_settings['model'] or model_names[0]

    parser = argparse.ArgumentParser(description='Chat with local language models.')
    parser.add_argument('--model', '-m', choices=model_names, help='Language model to chat with.')
    parser.add_argument('--chats-path', type=str, help='Directory to store chats.')
    parser.add_argument('--prompt-history', type=str, help='File to store prompt history.')
    parser.set_defaults(**user_settings)

    subparsers = parser.add_subparsers(help='Sub Commands')
    parser_settings = subparsers.add_parser('settings', help='Manage Charla settings')
    parser_settings.add_argument('--show', action='store_true', help='Show user settings.')
    parser_settings.set_defaults(func=config.manage)

    argv = parser.parse_args()

    # Make sure model is installed
    if argv.model not in model_names:
        sys.exit(f'Model {argv.model} is not installed.')

    argv.func(argv)

    context = []  # Store conversation history to make the model context aware
    output = [f'# Chat with: {argv.model}\n']  # List to store output text

    history = Path(argv.prompt_history)
    config.mkdir(history.parent, exist_ok=True, parents=True)
    session = chat.prompt_session(history)
    print_fmt('Chat with:', HTML(f'<ansigreen>{argv.model}</ansigreen>'), '\n')

    while True:
        try:
            user_input = session.prompt()
            if not user_input:
                continue

            output.append(f'{chat.t_prompt}{user_input}\n')
            print(f'\n{chat.t_response}\n')
            context = chat.generate(argv.model, user_input, context, output)
            print('\n')
        # Exit program on CTRL-C and CTRL-D
        except (KeyboardInterrupt, EOFError):
            break

    config.mkdir(argv.chats_path, exist_ok=True, parents=True)
    chat.save(argv.chats_path, output, argv.model)

    print_fmt(HTML('<b>Exiting program.</b>'))
    sys.exit()


if __name__ == '__main__':
    main()
