#!/usr/bin/env python
import argparse
import json
import sys

from charla import chat, config
from charla.__about__ import __version__


def handle_models(argv: argparse.Namespace):
    """Handler for models subcommand."""

    if argv.verbose:
        print(json.dumps(argv.models, indent=4))
    else:
        print('\n'.join(argv.model_names))


def main():
    """Create and execute command line interface."""

    if (models := chat.available_models()) is None:
        sys.exit('No language models available.')
    model_names = [m['name'] for m in models]

    user_settings = config.settings(config.load())
    user_settings['model'] = user_settings['model'] or model_names[0]

    # Allow names without version spec, i.e. llama3:latest -> llama3
    allowed_model_names = set(model_names) | {n.split(':')[0] for n in model_names}

    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument('--verbose', '-v', action='store_true', help='Verbose program output.')

    parser = argparse.ArgumentParser(description='Chat with local language models.')
    parser.add_argument('--model', '-m',
                        metavar='MODEL',
                        choices=allowed_model_names,
                        help='Name of language model to chat with.')
    parser.add_argument('--chats-path', type=str, help='Directory to store chats.')
    parser.add_argument('--prompt-history', type=str, help='File to store prompt history.')
    parser.add_argument('--multiline', action='store_true', help='User multiline mode.')
    parser.add_argument('--system-prompt', '-sp',
                        type=argparse.FileType(),
                        help='File that contains system prompt to use.')
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    parser.set_defaults(**user_settings, func=chat.run)

    subparsers = parser.add_subparsers(help='Sub Commands')

    parser_settings = subparsers.add_parser('settings', help='Show current settings.')
    parser_settings.add_argument('--location', action='store_true', help='Show location of settings file.')
    parser_settings.set_defaults(func=config.manage)

    parser_models = subparsers.add_parser('models', parents=[parent], help='Show available models.')
    parser_models.set_defaults(func=handle_models, models=models, model_names=model_names)

    argv = parser.parse_args()

    # Make sure model is installed
    if argv.model not in allowed_model_names:
        sys.exit(f'Model {argv.model} is not installed.')

    argv.func(argv)


if __name__ == '__main__':
    main()
