# UI texts and functions
from markdown import markdown
from prompt_toolkit import HTML
from prompt_toolkit import print_formatted_text as print_fmt

t_open = 'OPEN: '
t_open_toolbar = 'Add to prompt: '
t_prompt = 'PROMPT: '
t_prompt_ml = 'PROMPT \N{LATIN SUBSCRIPT SMALL LETTER M}\N{LATIN SUBSCRIPT SMALL LETTER L}: '
t_response = 'RESPONSE:'
t_system = 'SYSTEM PROMPT:'
t_help = '''
Press CTRL-C or CTRL-D to exit chat.
Press RETURN to send prompt in single line mode.
Press ALT+M to switch between single and multi line mode.
Press ALT+RETURN to send prompt in multi line mode.
Press CTRL-O to open a file or web page and append its content to the prompt.
Press CTRL-R or CTRL-S to search prompt history.
Press ↑ and ↓ to navigate previously entered prompts.
Press → to complete an auto suggested prompt.
'''

def highlight(text: str) -> str:
    return HTML(f'<ansigreen>{text}</ansigreen>')


def print_md(text: str) -> None:
    print_fmt(HTML(markdown(text, extensions=['extra'])))
