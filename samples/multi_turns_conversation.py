import asyncio
from typing import Any, Sequence

from agent_framework import ChatMessage, ChatMessageStoreProtocol

from maf_workflow.hosting import container
from maf_workflow.protocols.i_azure_open_ai_chat_client_service import (
    IAzureOpenAIChatClientService,
)

chat_client = container[IAzureOpenAIChatClientService].get_client()
SYSTEM_PROMPT = (
    "You are a helpful assistant that helps to answer questions around generativeAI."
)


class ChatMessageStore(ChatMessageStoreProtocol):
    def __init__(self):
        self.messages: list[ChatMessage] = []

    async def list_messages(self) -> list[ChatMessage]:
        return self.messages

    async def add_messages(self, messages: Sequence[ChatMessage]) -> None:
        for msg in messages:
            self.messages.append(msg)

    @classmethod
    async def deserialize(
        cls, serialized_store_state: Any, **kwargs: Any
    ) -> "ChatMessageStore":
        instance = ChatMessageStore()
        instance.messages = [
            ChatMessage.from_dict(msg_dict)
            for msg_dict in serialized_store_state.get("messages", [])
        ]
        return instance

    async def update_from_state(
        self, serialized_store_state: Any, **kwargs: Any
    ) -> None:
        self.messages += serialized_store_state.messages

    async def serialize(self, **kwargs: Any) -> Any:
        return {"messages": self.messages}


async def multi_turns():
    # this is where it starts
    agent = chat_client.create_agent(
        system_prompt=SYSTEM_PROMPT,
        chat_message_store_factory=lambda: ChatMessageStore(),  # custom store
    )
    thread1 = agent.get_new_thread()  # let's create a conversation thread

    message = input("User: ")
    while message.lower() not in ["exit", "quit"]:
        response = await agent.run(message, thread=thread1)
        print(f"Assistant: {response}")
        message = input("User: ")

    # serialize the conversation
    chat_data = await thread1.serialize()

    # resume the conversation
    resume_thread = await agent.deserialize_thread(chat_data)

    print("\nResuming the conversation...\n")
    message = input("User: ")
    while message.lower() not in ["exit", "quit"]:
        response = await agent.run(message, thread=resume_thread)
        print(f"Assistant: {response}")
        message = input("User: ")


if __name__ == "__main__":
    asyncio.run(multi_turns())
