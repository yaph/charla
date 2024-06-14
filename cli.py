#!/usr/bin/env python
from operator import itemgetter
from pathlib import Path
from time import time

from prompt_toolkit import PromptSession
from rich import print

import ollama


t_prompt = 'PROMPT: '
t_response = 'RESPONSE:'

models = None
if model_list := ollama.list()['models']:
    # Available models sorted by size
    models = [m for m in sorted(model_list, key=itemgetter('size'))]
else:
    print('No ollama models available.')
    quit()

#model = 'codegemma:latest'  # TODO: Store as user config
model = models[0]['name']  # TODO: Store as user config
context_length = 4096  # TODO: Derive this from model data when available

def generate(prompt, context, output):
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

    output.append(f'{t_response}\n\n{text}\n')
    return chunk['context']


def main():
    context = [] # the context stores a conversation history to make the model context aware
    session = PromptSession()
    output = []

    while True:
        user_input = session.prompt(t_prompt)

        if not user_input:
            if output:
                Path(f'chat-history-{int(time())}.txt').write_text('\n'.join(output))
            exit('No prompt entered, exit program.')

        output.append(f'{t_prompt}{user_input}\n')

        print(f'\n{t_response}\n')
        context = generate(user_input, context, output)
        print('\n')

        # Make sure the context doesn't get too long
        if len(context) > context_length:
            context = context[len(context)-context_length:]


if __name__ == '__main__':
    main()