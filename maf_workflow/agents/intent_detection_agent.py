from agent_framework import (
    AgentExecutor,
)
from agent_framework.azure import AzureOpenAIChatClient

from maf_workflow.models.intent_detection_result import IntentDetectionResult

SYSTEM_PROMPT = """
You are a helpful assistant who helps to identify the intention of a message.

The message must be one of the following:
- A social greeting such as "Hello", "Hi", "Good morning", etc.
- A inappropriate or harmful message such as hate speech, threats, harassment, insults,
  etc.
- A question or request for information.
- other general statements.

Response in JSON format with the following fields:
- message_content (string): The original message content.
- is_greeting (bool): true if the message is a greeting, false otherwise.
- is_inappropriate (bool): true if the message is inappropriate, false otherwise.
- is_question (bool): true if the message is a question or request for information,
  false otherwise.
- is_statement (bool): true if the message is a general statement, false otherwise.
- response (string): Generate a response to the message only if it is a greeting.
  For all other message types, return an empty string.
"""


def create_agent(chat_client: AzureOpenAIChatClient) -> AgentExecutor:
    return AgentExecutor(
        chat_client.create_agent(
            instructions=SYSTEM_PROMPT,
            response_format=IntentDetectionResult,
        ),
        id="spam_detection_agent",
    )
