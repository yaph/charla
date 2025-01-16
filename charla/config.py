import argparse
import json
import sys
from pathlib import Path

from platformdirs import user_cache_dir, user_config_path, user_documents_dir

NAME = 'charla'
PROVIDER_NAMES = ['ollama', 'github']

default_settings: dict = {
    'chats_path': user_documents_dir() + f'/{NAME}/chats',
    'message_limit': 20,
    'model': '',
    'multiline': False,
    'prompt_history': user_cache_dir(appname=NAME) + '/prompt-history.txt',
    'provider': PROVIDER_NAMES[0],
}
path_settings = user_config_path(NAME).joinpath('settings.json')


def load_settings(file: Path) -> dict:
    """Load settings from given JSON file and return them as a dict."""
    if file.exists():
        try:
            return json.loads(file.read_text())
        except json.decoder.JSONDecodeError as err:
            print(f'Settings could not be read. {err}')
    return {}


def manage(argv: argparse.Namespace) -> None:
    """Handler for settings subcommand."""

    if argv.location:
        print(path_settings)
    else:
        current_settings = {k: v for k, v in vars(argv).items() if k in default_settings}
        out = json.dumps(current_settings, indent=4)
        if argv.save:
            filename = '.charla.json'
            Path(filename).write_text(out)
            print(f'Saved settings in {filename}.')
        else:
            print(out)


def mkdir(path: Path, **kwds):
    """Wrapper for pathlib's mkdir."""

    try:
        path.mkdir(**kwds)
    except PermissionError as err:
        sys.exit(str(err))


def settings(current_settings: dict) -> dict:
    """Return settings based on user input."""

    default_settings.update(current_settings)
    return default_settings


def user_settings() -> dict:
    """Return settings from user config and current directory settings files, if they exist."""

    settings = load_settings(path_settings)
    settings.update(load_settings(Path('.charla.json')))
    return settings
