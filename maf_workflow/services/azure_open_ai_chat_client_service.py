from dataclasses import dataclass
from typing import Any

from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import DefaultAzureCredential
from lagom.environment import Env

from maf_workflow.protocols.i_azure_open_ai_chat_client_service import (
    IAzureOpenAIChatClientService,
)


class AzureOpenAIChatClientServiceEnv(Env):
    azure_openai_endpoint: str
    azure_openai_chat_deployment_name: str
    azure_openai_api_version: str = "2025-04-01-preview"
    azure_openai_api_key: str | None = None


@dataclass
class AzureOpenAIChatClientService(IAzureOpenAIChatClientService):
    env: AzureOpenAIChatClientServiceEnv

    def get_client(self) -> AzureOpenAIChatClient:
        params: dict[str, Any] = {
            "endpoint": self.env.azure_openai_endpoint,
            "deployment_name": self.env.azure_openai_chat_deployment_name,
            "api_version": self.env.azure_openai_api_version,
        }

        if self.env.azure_openai_api_key:
            params["api_key"] = self.env.azure_openai_api_key
        else:
            params["credential"] = DefaultAzureCredential()

        return AzureOpenAIChatClient(**params)
