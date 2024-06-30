import json

from functools import lru_cache

from platformdirs import user_cache_dir, user_config_path, user_documents_dir


name = 'charla'

default_settings = {
    'model': '',
    'chats_path': user_documents_dir() + f'/{name}/chats',
    'prompt_history': user_cache_dir(appname=name) + '/prompt-history.txt'
}

@lru_cache
def load() -> dict | None:
    p_settings = user_config_path('charla').joinpath('settings.json')
    if p_settings.exists():
        return json.loads(p_settings.read_text())
    return None


def manage(**argv):
    print('Hi')
    #breakpoint()
    #pass


def setting(key: str, value: str | None = None) -> str:
    user_settings = load()
    return value if value else user_settings.get(key, default_settings[key])


