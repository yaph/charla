# README

**charla** is a chat applications that uses `ollama` as a backend for serving language models. `ollama` must be running and you need to have at least one language model installed.

## Features

* Navigate through previously entered prompts using the up-arrow key on your keyboard.entered items.

## ollama API

Installed models:

     curl http://localhost:11434/api/tags

Model info:

    curl http://localhost:11434/api/show -d '{"name": "phi3"}'