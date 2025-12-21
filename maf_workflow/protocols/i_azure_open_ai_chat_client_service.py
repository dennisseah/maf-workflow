from typing import Protocol

from agent_framework.azure import AzureOpenAIChatClient


class IAzureOpenAIChatClientService(Protocol):
    def get_client(self) -> AzureOpenAIChatClient:
        """
        Returns for Azure OpenAI Chat Client

        :return: AzureOpenAIChatClient
        """
        ...
