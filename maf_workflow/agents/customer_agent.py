from agent_framework import (
    AgentExecutor,
)
from agent_framework.azure import AzureOpenAIChatClient

from maf_workflow.models.question_response import QuestionResponse

SYSTEM_PROMPT = """
You are a helpful assistant who helps users with answering questions.
Do you help to provide professional answers.

Response in JSON format with the following fields:
- user_question (string): The original question asked by the user.
- response (string): Provide a detailed and professional answer to the user's question.
"""


def create(chat_client: AzureOpenAIChatClient) -> AgentExecutor:
    return AgentExecutor(
        chat_client.create_agent(
            instructions=SYSTEM_PROMPT,
            response_format=QuestionResponse,
        ),
        id="customer_agent",
    )
