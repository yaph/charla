#!/usr/bin/env python
import io
from contextlib import redirect_stdout, suppress
from pathlib import Path

from charla import cli

start = '<!-- START: DO NOT EDIT -->'
end = '<!-- END: DO NOT EDIT -->'
quote = '```'

f = io.StringIO()
with redirect_stdout(f), suppress(SystemExit):
    cli.main(['-h'])
help_text = f.getvalue().replace('add_help_to_readme.py', 'charla')

readme_file = Path('README.md')
readme_content = readme_file.read_text()

p_start = readme_content.partition(start)[:2]
p_end = readme_content.partition(end)[1:]
p_all = (*p_start, f'\n{quote}text\n{help_text}\n{quote}\n', *p_end)

readme_file.write_text(''.join(p_all))
