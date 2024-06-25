#!/usr/bin/env python
import argparse
import sys

from prompt_toolkit import HTML, print_formatted_text as print_fmt

from charla import util


def main():
    if (models := util.available_models()) is None:
        sys.exit('No language models available.')
    model_names = [m['name'] for m in models]

    parser = argparse.ArgumentParser(description='Chat with local language models.')
    parser.add_argument('--model', '-m',
                        choices=model_names,
                        default=model_names[0],
                        help='Language model to chat with.')
    argv = parser.parse_args()

    context = [] # Store conversation history to make the model context aware
    output = [f'# Chat with: {argv.model}\n']  # List to store output text

    session = util.prompt_session()
    print_fmt('Chat with:', HTML(f'<ansigreen>{argv.model}</ansigreen>'), '\n')

    while True:
        try:
            user_input = session.prompt()
            if not user_input:
                continue

            output.append(f'{util.t_prompt}{user_input}\n')
            print(f'\n{util.t_response}\n')
            context = util.generate(argv.model, user_input, context, output)
            print('\n')
        # Exit program on CTRL-C and CTRL-D
        except (KeyboardInterrupt, EOFError):
            break

    util.save_chat(output)
    print_fmt(HTML('<b>Exiting program.</b>'))
    sys.exit()


if __name__ == '__main__':
    main()
