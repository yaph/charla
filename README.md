# Charla

[![PyPI - Version](https://img.shields.io/pypi/v/charla.svg)](https://pypi.org/project/charla)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/charla.svg)](https://pypi.org/project/charla)

**charla** is a chat applications that uses `ollama` as a backend for serving language models. `ollama` must be running and you need to have at least one language model installed.

## Installation

```console
pipx install charla
```

## Features

* Chat with local language model.
* Navigate previously entered prompts using the up-arrow key on your keyboard.

## ollama API

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
