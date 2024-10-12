#!/usr/bin/env python
import argparse

from charla import chat, config
from charla.__about__ import __version__


def main():
    """Create and execute command line interface."""

    user_settings = config.settings(config.load())

    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument('--verbose', '-v', action='store_true', help='Verbose program output.')

    parser = argparse.ArgumentParser(description='Chat with local language models.')
    parser.add_argument('--model', '-m', type=str, help='Name of language model to chat with.')
    parser.add_argument('--chats-path', type=str, help='Directory to store chats.')
    parser.add_argument('--prompt-history', type=str, help='File to store prompt history.')
    parser.add_argument('--provider', type=str, help='Name of the provider to use.')
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

    argv = parser.parse_args()
    argv.func(argv)


if __name__ == '__main__':
    main()
