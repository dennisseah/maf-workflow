import asyncio
from typing import Never

from agent_framework import (
    WorkflowBuilder,
    WorkflowContext,
    executor,
)

from maf_workflow.hosting import container
from maf_workflow.protocols.i_azure_open_ai_chat_client_service import (
    IAzureOpenAIChatClientService,
)

chat_client = container[IAzureOpenAIChatClientService].get_client()


@executor(id="fact_executor")
async def fact_executor(text: str, ctx: WorkflowContext[str]) -> None:
    instructions = (
        "You're an expert fact provider. Given a user's query, provide "
        "concise and accurate factual information about the country or place."
    )
    agent = chat_client.create_agent(instructions=instructions, name="fact_executor")

    response = await agent.run(text)
    await ctx.send_message(response.messages[0].contents[0].text)  # type: ignore


@executor(id="summarize_executor")
async def summarize_executor(text: str, ctx: WorkflowContext[Never, str]) -> None:
    instructions = (
        "Summarize the following text. limit your summary to 50 words or less."
    )
    agent = chat_client.create_agent(
        instructions=instructions, name="summarize_executor"
    )
    response = await agent.run(text)
    await ctx.yield_output(response.messages[0].contents[0].text)  # type: ignore


async def main() -> None:
    # Begin by building the workflow
    workflow = (
        WorkflowBuilder()
        .add_edge(fact_executor, summarize_executor)
        .set_start_executor(fact_executor)
        .build()
    )

    # 4) Run the workflow with a sample user query
    output = await workflow.run("We are planning a trip to Japan.")
    for o in output:
        if o.data:
            print(f"\033[32m{o.data}\033[0m")


if __name__ == "__main__":
    asyncio.run(main())
