#!/usr/bin/env python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential

import charla.ui as ui


token = os.environ['GITHUB_TOKEN']
endpoint = 'https://models.inference.ai.azure.com'

# Pick one of the Azure OpenAI models from the GitHub Models service
model_name = 'gpt-4o-mini'

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)


def generate(model: str, prompt: str, context: list, output: list, system=None) -> list:
    """Generate and print a response to the prompt and return the context."""

    if system:
        context.append(SystemMessage(content=system))

    context.append(UserMessage(content=prompt))

    response = client.complete(
        messages=context,
        model=model_name
    )

    text = response.choices[0].message.content
    print(text)

    context.append(AssistantMessage(content=text))
    output.append(ui.response(text))

    return context
