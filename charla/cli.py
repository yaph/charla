#!/usr/bin/env python
from prompt_toolkit import PromptSession
from rich import print

import argparse

import util


def main():
    if (models := util.available_models()) is None:
        print('No language models available.')
        quit()
    model_names = [m['name'] for m in models]

    parser = argparse.ArgumentParser(description='Chat with local language models.')
    parser.add_argument('--model', '-m', choices=model_names, default=model_names[0],
                        help='Language model to chat with.')
    argv = parser.parse_args()

    context = [] # the context stores a conversation history to make the model context aware
    output = []

    print(f'Starting chat with: {argv.model}\n')
    session = PromptSession()

    while True:
        user_input = session.prompt(util.t_prompt)

        if not user_input:
            util.save_chat(output)
            exit('No prompt entered, exit program.')

        output.append(f'{util.t_prompt}{user_input}\n')

        print(f'\n{util.t_response}\n')
        context = util.generate(argv.model, user_input, context, output)
        print('\n')


if __name__ == '__main__':
    main()