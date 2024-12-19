# Charla: Chat with Language Models in a Terminal

[![PyPI - Version](https://img.shields.io/pypi/v/charla.svg)](https://pypi.org/project/charla)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/charla.svg)](https://pypi.org/project/charla)

**Charla** is a terminal based application for chatting with language models. Charla integrates with Ollama and GitHub Models for exchanging messages with model services.

![preview](https://geeksta.net/img/tools/charla-chat-demo.gif)

## Features

* Terminal-based chat system that supports context aware conversations with language models.
* Support for local models via Ollama and remote models via GitHub Models.
* Chat sessions are saved as markdown files in the user's documents directory when ending a chat.
* Prompt history is saved and previously entered prompts are auto-suggested.
* Switch between single-line and multi-line input modes without interrupting the chat session.
* Store user preferences in user config or current directory settings files.
* Provide a system prompt for a chat session.
* Load content from local files and web pages to append to prompts.

## Installation

To use Charla with models on your computer, you need a running installation of the [Ollama server](https://ollama.com/download) and at least one supported language model must be installed. For [GitHub Models](https://github.com/marketplace/models) you need access to the service and a GitHub token. Please refer to the documentation of the service provider you want to use for installation and setup instructions.

Install Charla using `pipx`:

```console
pipx install charla
```

For GitHub models, set the environment variable GITHUB_TOKEN to your token. In Bash enter:

```console
export GITHUB_TOKEN=YOUR_GITHUB_TOKEN
```

## Usage

After successful installation and setup you can launch the chat console with the `charla` command in your terminal.

If you use Charla with Ollama, the default provider, you only need to specify the model to use, e.g.:

```console
charla -m phi3
```

If you want to use GitHub Models, you have to set the provider:

```console
charla -m gpt-4o --provider github
```

You can set a default model and change the default provider in your user settings file.

## Settings

Settings can be specified as command line arguments and in the settings files. Command line arguments have the highest priority. The location of your user config settings file depends on your operating system. Use the following command to show the location:

```console
charla settings --location
```

You can also store settings in the current working directory in a file named `.charla.json`. The settings in this local override the user config settings.

To save the current settings to a `.charla.json` file in the current directory, use the `--save` argument:

```console
charla settings --save
```

Example settings for using OpenAI's GPT-4o model and the GitHub Models service by default.

```json
{
    "model": "gpt-4o",
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
curl http://localhost:11434/api/tags | python -m json.tool
```

Model info:

```console
curl http://localhost:11434/api/show -d '{"name": "phi3"}'
```

## License

Charla is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
