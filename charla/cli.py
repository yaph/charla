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

    parser = argparse.ArgumentParser(description='Chat with local language models.')
    parser.add_argument('--model', '-m', choices=model_names, help='Language model to chat with.')
    argv = parser.parse_args()

    # Determine model
    model = config.setting('model', argv.model)
    if not model:
        model = model_names[0]
    elif model not in model_names:
        sys.exit(f'Model {model} is not installed.')

    context = []  # Store conversation history to make the model context aware
    output = [f'# Chat with: {model}\n']  # List to store output text

    history = Path(config.setting('prompt_history'))
    history.parent.mkdir(exist_ok=True, parents=True)
    session = chat.prompt_session(history)

    print_fmt('Chat with:', HTML(f'<ansigreen>{model}</ansigreen>'), '\n')

    while True:
        try:
            user_input = session.prompt()
            if not user_input:
                continue

            output.append(f'{chat.t_prompt}{user_input}\n')
            print(f'\n{chat.t_response}\n')
            context = chat.generate(model, user_input, context, output)
            print('\n')
        # Exit program on CTRL-C and CTRL-D
        except (KeyboardInterrupt, EOFError):
            break

    chats_path = Path(config.setting('chats_path'))
    chats_path.mkdir(exist_ok=True, parents=True)
    chat.save(chats_path, output, model)

    print_fmt(HTML('<b>Exiting program.</b>'))
    sys.exit()


if __name__ == '__main__':
    main()
