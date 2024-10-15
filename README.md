# Charla: Chat with Language Models in a Terminal

[![PyPI - Version](https://img.shields.io/pypi/v/charla.svg)](https://pypi.org/project/charla)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/charla.svg)](https://pypi.org/project/charla)

**Charla** is a terminal based application for chatting with language models. Charla integrates with [Ollama](https://ollama.com/) and [GitHub Models](https://github.com/marketplace/models) for exchanging messages with model services.

To use Charla with models on your computer, you need a running installation of the `ollama` server and at least one supported language model must be installed. For GitHub Models you need access to the service and a GitHub token. Please refer to the documentation of the service provider you want to use for installation and setup instructions.

![preview](https://geeksta.net/img/tools/charla-chat-demo.gif)

## Installation

Install Charla using `pipx`:

```console
pipx install charla
```

## Usage

Launch the chat console by typing `charla` in your terminal.

## Features

* Terminal-based chat system that supports context aware conversations with language models.
* Support for local models via Ollama and remote models via GitHub Models.
* Chat sessions are saved as markdown files in the user's documents directory when ending a chat.
* Prompt history is saved and previously entered prompts are auto-suggested.
* Switch between single-line and multi-line input modes without interrupting the chat session.
* Store default user preferences in a settings file.
* Provide a system prompt for a chat session.
* Load content from local files and web pages to append to prompts.

## Configuration

```json
{
    "model": "phi3",
    "chats_path": "./chats",
    "prompt_history": "./prompt-history.txt",
    "provider": "github",
    "message_limit": 20,
    "multiline": false
}
```

## CLI Help

Output of `charla -h` with information on all available command line options.

<!-- START: DO NOT EDIT -->
```text
usage: charla [-h] [--model MODEL] [--chats-path CHATS_PATH] [--prompt-history PROMPT_HISTORY]
                             [--provider PROVIDER] [--message-limit MESSAGE_LIMIT] [--multiline] [--system-prompt SYSTEM_PROMPT]
                             [--version]
                             {settings} ...

Chat with language models.

positional arguments:
  {settings}            Sub Commands
    settings            Show current settings.

options:
  -h, --help            show this help message and exit
  --model MODEL, -m MODEL
                        Name of language model to chat with.
  --chats-path CHATS_PATH
                        Directory to store chats.
  --prompt-history PROMPT_HISTORY
                        File to store prompt history.
  --provider PROVIDER   Name of the provider to use.
  --message-limit MESSAGE_LIMIT
                        Maximum number of messages to send to GitHub Models service.
  --multiline           Use multiline mode.
  --system-prompt SYSTEM_PROMPT, -sp SYSTEM_PROMPT
                        File that contains system prompt to use.
  --version             show program's version number and exit

```
<!-- END: DO NOT EDIT -->

## Development

Run the command-line interface directly from the project source without installing the package:

```console
python -m charla.cli
```

### ollama API

Installed models:

```console
curl http://localhost:11434/api/tags
```

Model info:

```console
curl http://localhost:11434/api/show -d '{"name": "phi3"}'
```

## License

Charla is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
