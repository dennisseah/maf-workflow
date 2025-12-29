import asyncio

from agent_framework import Context, ContextProvider
from agent_framework._memory import AggregateContextProvider

from maf_workflow.hosting import container
from maf_workflow.protocols.i_azure_open_ai_chat_client_service import (
    IAzureOpenAIChatClientService,
)

# sample code to demonstrate custom context providers
# that inject dynamic information into each agent invocation
# based on user profile data, Agent generates favorite songs based on age and gender

chat_client = container[IAzureOpenAIChatClientService].get_client()
SYSTEM_PROMPT = (
    "You are a helpful assistant that helps to generate a list of favorite songs "
    "based on user profiles."
)

old_guy = "john_doe"
yound_lady = "mary_ann"


class UserAgeProvider(ContextProvider):
    def __init__(self, user_id: str):
        self.user_id = user_id

    async def invoking(self, messages, **kwargs) -> Context:
        # base on the user_id, fetch user preferences from a database or service
        # for now, we will mock this behavior
        user_age = 60 if self.user_id == old_guy else 16

        # 2. Return a Context object with the new information
        # This will be merged into the prompt for this specific invocation
        return Context(
            instructions=f"Age: {user_age}.",
            messages=[],  # optionally, inject additional ChatMessage objects here
            tools=[],  # optionally, dynamically add tools for this turn
        )

    async def invoked(
        self,
        request_messages,
        response_messages=None,
        invoke_exception=None,
        **kwargs,
    ) -> None:
        # just to demonstrate, we can get the request and response messages here
        req_content = request_messages[0].contents[0].text  # type: ignore
        res_content = response_messages[0].contents[0].text  # type: ignore

        print("\033[92m----------------------------------------\033[0m")
        print(f"\033[92mInvocation completed for user {self.user_id}\033[0m")
        print(f"\033[92m[DEBUG] Request messages: {req_content}\033[0m")
        print(f"\033[92m[DEBUG] Response messages: {res_content}\033[0m")
        print("\033[92m----------------------------------------\033[0m")
        print()
        print()


class UserGenderProvider(ContextProvider):
    def __init__(self, user_id: str):
        self.user_id = user_id

    async def invoking(self, messages, **kwargs) -> Context:
        user_gender = "Male" if old_guy else "Female"

        return Context(
            instructions=f"Gender: {user_gender}.",
        )

    async def invoked(
        self,
        request_messages,
        response_messages=None,
        invoke_exception=None,
        **kwargs,
    ) -> None:
        pass


async def main():
    "old_guy is a 60-year-old male otherwise the profile is a 16-year-old female"
    user_id = old_guy
    agent = chat_client.create_agent(
        system_prompt=SYSTEM_PROMPT,
        context_providers=[
            UserAgeProvider(user_id),
            UserGenderProvider(user_id),
        ],
    )
    # since we have 2 context providers, the agent combine both context during
    # invocation, an AggregateContextProvider is created internally
    #
    print(isinstance(agent.context_provider, AggregateContextProvider))

    # Run the agent; the 'invoking' method will trigger automatically
    result = await agent.run("list 5 favorite songs")
    print(result.text)


if __name__ == "__main__":
    asyncio.run(main())
