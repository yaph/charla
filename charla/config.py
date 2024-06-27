from platformdirs import user_cache_dir, user_documents_dir

from charla import __about__


name = __about__.__name__

default_settings = {
    'model': '',
    'chats_path': user_documents_dir() + f'/{name}/chats',
    'prompt_history': user_cache_dir(appname=name) + '/prompt-history.txt'
}


def setting(key: str, value: str = None) -> str:
    return value if value else default_settings.get(key)

