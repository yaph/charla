from charla import chat


# def test_available_models():
#     models = chat.available_models()
#     assert len(models)
#     assert 'name' in models[0]


def test_prompt_session():
    session = chat.prompt_session('cache/prompt-history.txt')
    assert session.message == chat.t_prompt
