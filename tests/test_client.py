import pytest

from charla.client import Client
from charla.client.github import GithubClient
from charla.client.ollama import OllamaClient


def test_client_init_error():
    """Ensure Client class cannot be instantiated directly."""

    with pytest.raises(TypeError):
        Client(model='phi3')


def test_client_ollama_init():
    client = OllamaClient(model='phi3')
    assert hasattr(client, 'context')


def test_client_azure():
    client = GithubClient(model='gpt-4o', provider='github', message_limit=10)
    assert hasattr(client.client, 'close')
