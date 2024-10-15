import pytest

from charla.client import Client
from charla.client.github import AzureClient
from charla.client.ollama import OllamaClient


def test_client_init_error():
    """Ensure Client class cannot be instantiated directly."""

    with pytest.raises(TypeError):
        Client(model='phi3')


def test_client_ollama_init():
    client = OllamaClient(model='phi3')
    assert hasattr(client, 'context')


def test_client_azure():
    client = AzureClient(model='gpt-4o', message_length=10)
    assert hasattr(client.client, 'close')
