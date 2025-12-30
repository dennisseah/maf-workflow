import asyncio
from typing import Never

from agent_framework import (
    Executor,
    WorkflowBuilder,
    WorkflowContext,
    handler,
)
from agent_framework.azure import AzureOpenAIChatClient

from maf_workflow.hosting import container
from maf_workflow.protocols.i_azure_open_ai_chat_client_service import (
    IAzureOpenAIChatClientService,
)


class ExecutorBase(Executor):
    def __init__(self, chat_client: AzureOpenAIChatClient, id: str, instructions: str):
        self.agent = chat_client.create_agent(instructions=instructions, name=id)
        super().__init__(agent=self.agent, id=id)

    @handler
    async def handle(self, user_query: str, ctx: WorkflowContext[str]):
        response = await self.agent.run(user_query)
        await ctx.send_message(response.messages[0].contents[0].text)  # type: ignore


class FactExecutor(ExecutorBase):
    # FactExecutor provides concise factual information
    def __init__(self, chat_client: AzureOpenAIChatClient):
        instructions = (
            "You're an expert fact provider. Given a user's query, provide "
            "concise and accurate factual information about the country or place."
            "Keep your responses to 50 words or less."
        )
        super().__init__(
            chat_client=chat_client, id="fact_executor", instructions=instructions
        )


class PoemExecutor(ExecutorBase):
    # PoemExecutor creates a short, engaging poem
    def __init__(self, chat_client: AzureOpenAIChatClient):
        instructions = (
            "You are a creative poet. Given a user's query, compose a short and "
            "engaging poem that captures the essence of the topic. "
            "Keep your responses to 50 words or less."
        )
        super().__init__(
            chat_client=chat_client, id="poem_executor", instructions=instructions
        )


class Dispatcher(Executor):
    # Dispatcher broadcasts the user query to multiple executors
    @handler
    async def handle(self, user_query: str, ctx: WorkflowContext[str]):
        await ctx.send_message(user_query)


class Aggregator(Executor):
    # Aggregator combines outputs from multiple executors
    @handler
    async def handle(self, results: list[str], ctx: WorkflowContext[Never, str]):
        combined = "\n\n".join(results)
        await ctx.yield_output(combined)


async def main() -> None:
    # 1) Initialize executors with Azure OpenAI Chat client
    chat_client = container[IAzureOpenAIChatClientService].get_client()

    # 2) Create dispatcher, executors, and aggregator
    dispatcher = Dispatcher(id="dispatcher")
    fact_executor = FactExecutor(chat_client)
    poem_executor = PoemExecutor(chat_client)
    aggregator = Aggregator(id="aggregator")

    # 3) Build a simple fan out and fan in workflow
    workflow = (
        WorkflowBuilder()
        .set_start_executor(dispatcher)
        .add_fan_out_edges(dispatcher, [fact_executor, poem_executor])
        .add_fan_in_edges([fact_executor, poem_executor], aggregator)
        .build()
    )

    # 4) Run the workflow with a sample user query
    output = await workflow.run("We are planning a trip to Japan.")
    for o in output:
        if o.data:
            print(o.data)


if __name__ == "__main__":
    asyncio.run(main())
