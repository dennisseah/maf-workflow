import pytest
from pytest_mock import MockerFixture

from maf_workflow.services.azure_open_ai_chat_client_service import (
    AzureOpenAIChatClientService,
    AzureOpenAIChatClientServiceEnv,
)


@pytest.mark.parametrize("api_key", ["test-api-key", None])
def test_get_client(api_key, mocker: MockerFixture) -> None:
    mock_client = mocker.patch(
        "maf_workflow.services.azure_open_ai_chat_client_service.AzureOpenAIChatClient"
    )
    mock_def_cred = mocker.patch(
        "maf_workflow.services.azure_open_ai_chat_client_service.DefaultAzureCredential"
    )
    env = AzureOpenAIChatClientServiceEnv(
        azure_openai_endpoint="https://test-endpoint.openai.azure.com/",
        azure_openai_chat_deployment_name="test-deployment",
        azure_openai_api_version="2025-04-01-preview",
        azure_openai_api_key=api_key,
    )
    service = AzureOpenAIChatClientService(env=env)
    client = service.get_client()

    assert client is not None
    mock_client.assert_called_once()

    if api_key:
        assert mock_def_cred.call_count == 0
    else:
        mock_def_cred.assert_called_once()
