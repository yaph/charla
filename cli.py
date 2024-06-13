#!/usr/bin/env python
import ollama

# ollama must be running for this to work, run `ollama serve`
#model = 'codegemma:latest' # TODO: Store as user config
model = 'phi3:latest' # TODO: Store as user config
context_length = 4096

def generate(prompt, context):
    stream = ollama.generate(
        model=model,
        prompt=prompt,
        context=context,
        stream=True,
    )
    for chunk in stream:
        if not chunk['done']:
            print(chunk['response'], end='', flush=True)
        else:
            return chunk['context']

def main():
    context = [] # the context stores a conversation history to make the model context aware
    while True:
        user_input = input("Enter a prompt: ")
        if not user_input:
            exit()
        print()
        context = generate(user_input, context)
        # Make sure the context doesn't get too long
        if len(context) > context_length:
            context = context[len(context)-context_length:]
        print()

if __name__ == "__main__":
    main()