import argparse
import json
import sys
from pathlib import Path

from platformdirs import user_cache_dir, user_config_path, user_documents_dir

NAME = 'charla'

default_settings: dict = {
    'model': '',
    'chats_path': user_documents_dir() + f'/{NAME}/chats',
    'prompt_history': user_cache_dir(appname=NAME) + '/prompt-history.txt',
    'multiline': False
}
path_settings = user_config_path(NAME).joinpath('settings.json')


def load() -> dict:
    """Return settings from settings file, if it exists."""

    if path_settings.exists():
        try:
            return json.loads(path_settings.read_text())
        except json.decoder.JSONDecodeError as err:
            print(f'Settings could not be read. {err}')
    return {}


def mkdir(path: Path, **kwds):
    """Wrapper for pathlib's mkdir."""

    try:
        path.mkdir(**kwds)
    except PermissionError as err:
        sys.exit(str(err))


def settings(user_settings: dict) -> dict:
    """Return settings based on user input."""

    default_settings.update(user_settings)
    return default_settings


def manage(argv: argparse.Namespace) -> None:
    """Handler for settings subcommand."""

    if argv.location:
        print(path_settings)
    else:
        user_settings = {k: v for k, v in vars(argv).items() if k in default_settings}
        print(json.dumps(user_settings, indent=4))
