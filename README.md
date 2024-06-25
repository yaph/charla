# Charla: Terminal-Based Chat Application with Ollama Backend Integration

[![PyPI - Version](https://img.shields.io/pypi/v/charla.svg)](https://pypi.org/project/charla)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/charla.svg)](https://pypi.org/project/charla)

**Charla** is a terminal based chat application that seamlessly integrates with `ollama`, a powerful backend designed to serve advanced language models. To use Charla, ensure that the `ollama` server is running and at least one language model is installed.

## Installation

Install Charla using `pipx`:

```console
pipx install charla
```

## Usage

Launch the chat console by typing `charla` in your terminal, or view all available command line options with `charla -h`.

## Features

* Terminal-based chat system that supports context aware conversations using local language models.
* Chat history is saved to a file in the current working directory.
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

`charla` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
