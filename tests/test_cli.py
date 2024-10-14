from charla.cli import main


def test_cli_help(capsys):
    try:
        main(['-h'])
    except SystemExit:
        pass
    output = capsys.readouterr().out
    assert 'language model' in output