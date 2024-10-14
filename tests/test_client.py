import pytest

from charla.client import Client
from charla.client.ollama import OllamaClient
from charla.client.github import AzureClient


def test_client_init_error():
    """Ensure Client class cannot be instantiated directly."""

    with pytest.raises(TypeError):
        Client(model='phi3', context=[], output=[])


def test_client_ollama_init():
    context = []
    client = OllamaClient(model='phi3', context=context, output=[])
    assert context is client.context


def test_client_azure():
    context = []
    client = AzureClient(model='gpt-4o', context=context, output=[])

    assert hasattr(client.client, 'close')