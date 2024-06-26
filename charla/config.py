from platformdirs import user_cache_dir, user_documents_dir


default_settings = {
    'model': '',
    'chats_path': user_documents_dir() + '/charla/chats',
    'prompt_history': user_cache_dir(appname='charla') + '/prompt-history.txt'
}


def setting(name: str, value: str = None) -> str:
    return value if value else default_settings.get(name)

