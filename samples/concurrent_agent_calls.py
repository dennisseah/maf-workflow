import asyncio
from typing import Annotated, Any

from agent_framework import (
    AgentExecutorRequest,
    AgentExecutorResponse,
    ConcurrentBuilder,
    Executor,
    WorkflowContext,
    ai_function,
    handler,
)
from agent_framework.azure import AzureOpenAIChatClient
from pydantic import Field

from maf_workflow.hosting import container
from maf_workflow.protocols.i_azure_open_ai_chat_client_service import (
    IAzureOpenAIChatClientService,
)

ID_FACT_EXECUTOR = "fact_executor"
ID_POEM_EXECUTOR = "poem_executor"


@ai_function
def get_weather(
    location: Annotated[str, Field(description="The city name")],
) -> str:
    """Gets the current weather for a location."""
    return f"The weather in {location} is 72°F and sunny."


class ExecutorBase(Executor):
    def __init__(self, chat_client: AzureOpenAIChatClient, id: str, instructions: str):
        self.agent = chat_client.create_agent(instructions=instructions, name=id)
        super().__init__(agent=self.agent, id=id)

    @handler
    async def run(
        self, request: AgentExecutorRequest, ctx: WorkflowContext[AgentExecutorResponse]
    ) -> None:
        response = await self.agent.run(request.messages)
        full_conversation = list(request.messages) + list(response.messages)
        await ctx.send_message(
            AgentExecutorResponse(
                self.id, response, full_conversation=full_conversation
            )
        )


class FactExec(ExecutorBase):
    # inherit from ExecutorBase
    def __init__(self, chat_client: AzureOpenAIChatClient):
        instructions = (
            "You're an expert fact provider. Given a user's query, provide "
            "concise and accurate factual information about the country or place."
            "Keep your responses to 50 words or less."
        )
        super().__init__(
            chat_client=chat_client, id=ID_FACT_EXECUTOR, instructions=instructions
        )


class PoemExec(ExecutorBase):
    # inherit from ExecutorBase
    def __init__(self, chat_client: AzureOpenAIChatClient):
        instructions = (
            "You are a creative poet. Given a user's query, compose a short and "
            "engaging poem that captures the essence of the topic. "
            "Keep your responses to 50 words or less."
        )
        super().__init__(
            chat_client=chat_client, id=ID_POEM_EXECUTOR, instructions=instructions
        )


async def consolidates(results: list[Any]) -> str:
    # Extract one final assistant message per agent
    output: list[str] = []
    for r in results:
        output.append("")
        messages = getattr(r.agent_run_response, "messages", [])
        final_text = messages[-1].text
        exec_id = getattr(r, "executor_id")

        if exec_id == ID_FACT_EXECUTOR:
            output.append(f"Fact Expert Output:\n{final_text}")
        elif exec_id == ID_POEM_EXECUTOR:
            output.append(f"Poem Expert Output:\n{final_text}")

    return "\n".join(output)


async def main():
    # this is the entry point of the sample

    chat_client = container[IAzureOpenAIChatClientService].get_client()
    workflow = (
        ConcurrentBuilder()
        .participants(  # include multiple agents
            [FactExec(chat_client), PoemExec(chat_client)]
        )
        .with_aggregator(consolidates)  # combine results from both agents
        .build()
    )

    output = await workflow.run("We are planning a trip to Japan.")
    for o in output:
        if o.data:
            print(o.data)


if __name__ == "__main__":
    asyncio.run(main())
