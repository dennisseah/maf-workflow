import asyncio
from typing import Annotated

from agent_framework import ai_function
from pydantic import Field

from maf_workflow.hosting import container
from maf_workflow.protocols.i_azure_open_ai_chat_client_service import (
    IAzureOpenAIChatClientService,
)

chat_client = container[IAzureOpenAIChatClientService].get_client()


# function as tool
@ai_function(name="favorite_place", description="favorite place to visit")
def get_place(
    user_id: Annotated[
        str, Field(description="User id for determine the favourite place to visit.")
    ],
) -> str:
    return "Paris"  # assuming Paris is the favorite place for any user id


# agent as tool
tourist_guide_agent = chat_client.create_agent(
    name="tourist_guide_agent",
    instructions=(
        "You are a tourist guide. Provide 3 place of interests for a given location. "
        "Just name the places without any additional information."
    ),
).as_tool(
    name="tourist_guide_agent",
    description="Get 3 place of interests for a given location.",
)


async def main():
    agent = chat_client.create_agent(
        instructions=(
            "You are a travel assistant. Use the 'favorite_place' tool to figure out "
            "the user's favorite place to visit. And, the 'tourist_guide_agent' to get "
            "3 place of interests for that location. IMPORTANT: do not provide any "
            "more information."
        ),
        tools=[get_place, tourist_guide_agent],
    )
    result = await agent.run(
        "Tell me about my favorite place to visit. My user id is 123."
    )
    print(result.text)


if __name__ == "__main__":
    asyncio.run(main())
