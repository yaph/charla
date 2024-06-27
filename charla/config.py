from platformdirs import user_cache_dir, user_documents_dir


name = 'charla'

default_settings = {
    'model': '',
    'chats_path': user_documents_dir() + f'/{name}/chats',
    'prompt_history': user_cache_dir(appname=name) + '/prompt-history.txt'
}


def setting(key: str, value: str | None = None) -> str:
    return value if value else default_settings[key]

