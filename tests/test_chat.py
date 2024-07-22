import argparse

from charla import chat, config


def mock_args():
    p = argparse.ArgumentParser()
    p.set_defaults(**config.default_settings)
    return p.parse_args([])


def test_get_content_error():
    assert '' == chat.get_content('https://does-not-exist')
    assert '' == chat.get_content('does-not-exist.file')


def test_get_content_file():
    content = chat.get_content('./tests/test_chat.py')
    assert len(content)


def test_prompt_session():
    session = chat.prompt_session(mock_args())
    assert session.message == chat.t_prompt
