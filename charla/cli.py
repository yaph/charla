#!/usr/bin/env python
import argparse

from charla import chat, config
from charla.__about__ import __version__


def main(args=None) -> None:
    """Create and execute command line interface."""

    # Settings priority: cli args > user settings > default settings.
    user_settings = config.settings(config.user_settings())

    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument('--verbose', '-v', action='store_true', help='Verbose program output.')

    parser = argparse.ArgumentParser(description='Chat with language models.')
    parser.add_argument('--model', '-m', type=str, help='Name of language model to chat with.')
    parser.add_argument('--chats-path', type=str, help='Directory to store chats.')
    parser.add_argument('--prompt-history', type=str, help='File to store prompt history.')
    parser.add_argument('--provider', type=str, help='Name of the provider to use.')
    parser.add_argument(
        '--message-limit', type=int, help='Maximum number of messages to send to GitHub Models service.'
    )
    parser.add_argument('--multiline', action='store_true', help='Use multiline mode.')
    parser.add_argument(
        '--system-prompt', '-sp', type=str, help='File that contains system prompt to use.'
    )
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    parser.set_defaults(**user_settings, func=chat.run)

    subparsers = parser.add_subparsers(help='Sub Commands')

    parser_settings = subparsers.add_parser('settings', help='Show current settings.')
    parser_settings.add_argument('--location', action='store_true', help='Show location of settings file.')
    parser_settings.add_argument('--save', action='store_true', help='Save settings in ".charla.json" file.')
    parser_settings.set_defaults(func=config.manage)

    argv = parser.parse_args(args)
    argv.func(argv)


if __name__ == '__main__':
    main()
