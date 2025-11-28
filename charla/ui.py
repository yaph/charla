# UI texts and functions
import html
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


def print_html(text: str) -> None:
    print_fmt(HTML(text))


def print_md(text: str) -> None:
    # Escape characters like < and > in text to prevent HTML parser errors
    print_html(markdown(html.escape(text), extensions=['extra']))


def print_message(role: str, text: str) -> None:
    match role:
        case 'user':
            print(f'{t_prompt}{text}\n')
        case 'assistant':
            print(f'{t_response}\n')
            print_md(text)
        case 'system':
            print(f'{t_system}\n')
            print_md(text)
