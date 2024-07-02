import json
import sys

from platformdirs import user_cache_dir, user_config_path, user_documents_dir


name = 'charla'

default_settings = {
    'chats_path': user_documents_dir() + f'/{name}/chats',
    'prompt_history': user_cache_dir(appname=name) + '/prompt-history.txt'
}

def load() -> dict[str, str]:
    p_settings = user_config_path('charla').joinpath('settings.json')
    if p_settings.exists():
        try:
            return json.loads(p_settings.read_text())
        except json.decoder.JSONDecodeError as err:
            print(f'Settings could not be read. {err}')
    return {}


def get(user_settings: dict[str, str], key: str, value: str | None = None) -> str:
    return value if value else user_settings.get(key, '')


def mkdir(path, **kwds):
    try:
        path.mkdir(**kwds)
    except PermissionError as err:
        sys.exit(err)


def settings(user_settings: dict[str, str]) -> dict[str, str]:
    default_settings.update(user_settings)
    return default_settings
