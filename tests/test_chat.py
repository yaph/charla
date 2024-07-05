import argparse

from charla import chat, config


def mock_args():
    p = argparse.ArgumentParser()
    p.set_defaults(**config.default_settings)
    return p.parse_args([])


# def test_available_models():
#     models = chat.available_models()
#     assert len(models)
#     assert 'name' in models[0]


def test_prompt_session():
    session = chat.prompt_session(mock_args())
    assert session.message == chat.t_prompt
