import argparse
import json
import sys

from pathlib import Path

from platformdirs import user_cache_dir, user_config_path, user_documents_dir


name = 'charla'

default_settings = {
    'model': '',
    'chats_path': user_documents_dir() + f'/{name}/chats',
    'prompt_history': user_cache_dir(appname=name) + '/prompt-history.txt'
}

path_settings = user_config_path(name).joinpath('settings.json')


def load() -> dict[str, str]:
    if path_settings.exists():
        try:
            return json.loads(path_settings.read_text())
        except json.decoder.JSONDecodeError as err:
            print(f'Settings could not be read. {err}')
    return {}


def mkdir(path: Path, **kwds):
    try:
        path.mkdir(**kwds)
    except PermissionError as err:
        sys.exit(str(err))


def settings() -> dict[str, str]:
    default_settings.update(load())
    return default_settings


def manage(argv: argparse.Namespace) -> None:
    if argv.location:
        print(path_settings)
    else:
        user_settings = {k: v for k, v in vars(argv).items() if k in default_settings}
        print(json.dumps(user_settings, indent=4))
