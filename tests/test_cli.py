from contextlib import suppress

from charla.cli import main


def test_cli_help(capsys):
    with suppress(SystemExit):
        main(['-h'])
    output = capsys.readouterr().out
    assert 'language model' in output
