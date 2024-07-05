from charla import config


def test_settings():
    model = 'dummy'
    settings = config.settings({'model': model})
    assert settings['model'] == model
    assert isinstance(settings['multiline'], bool)
