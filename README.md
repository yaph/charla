# Charla: Chat with Language Models in a Terminal

[![PyPI - Version](https://img.shields.io/pypi/v/charla.svg)](https://pypi.org/project/charla)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/charla.svg)](https://pypi.org/project/charla)

**Charla** is a terminal based chat application that integrates with [Ollama](https://ollama.com/), a backend designed to serve language models. To use Charla, ensure that the `ollama` server is running and at least one language model is installed.

![preview](https://repository-images.githubusercontent.com/821132128/9b8c0c11-baaf-46ce-8681-de62d648281e)

## Installation

Install Charla using `pipx`:

```console
pipx install charla
```

## Usage

Launch the chat console by typing `charla` in your terminal, or view all available command line options with `charla -h`.

## Features

* Terminal-based chat system that supports context aware conversations using local language models.
* Chat sessions are saved as markdown files in the user's documents directory when ending a chat.
* Prompt history is saved and previously entered prompts are auto-suggested.
* Mode switching between single-line and multi-line input without interruption to your chat session.

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
