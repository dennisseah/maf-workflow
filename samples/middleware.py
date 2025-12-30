import asyncio
import json
from typing import Annotated, Awaitable, Callable, Never

from agent_framework import (
    AgentExecutor,
    AgentExecutorRequest,
    AgentExecutorResponse,
    ChatMessage,
    FunctionInvocationContext,
    Role,
    WorkflowBuilder,
    WorkflowContext,
    ai_function,
    executor,
)
from pydantic import BaseModel

from maf_workflow.hosting import container
from maf_workflow.protocols.i_azure_open_ai_chat_client_service import (
    IAzureOpenAIChatClientService,
)

# a sample use case: flight booking with priority boarding for gold members
# initialize chat client and user status
# use a middleware to modify the booking result based on user status
# that's gold member gets priority boarding
# the middleware intercepts the function invocation result
# and modifies the result to set priority_boarding = True

chat_client = container[IAzureOpenAIChatClientService].get_client()
is_gold_member = True


class BookingResult(BaseModel):
    # booking result from flight booking tool
    # default is priority_boarding = False
    # depends on user status, e.g., gold member or not, priority override
    # priority_boarding is set to True
    destination: str
    is_available: bool = True  # flight is available to make thing simple
    priority_boarding: bool = False
    priority_override: bool = False


@ai_function(description="Check flight availability for a destination city")
def booking_tool(destination: Annotated[str, "The destination city"]) -> str:
    # to make it simple, we assume all destinations have availability :-)
    result = {"destination": destination, "priority_boarding": False}
    return json.dumps(result)


async def priority_check_middleware(
    context: FunctionInvocationContext,
    next: Callable[[FunctionInvocationContext], Awaitable[None]],
) -> None:
    function_name = context.function.name
    print(f"\033[32m{function_name} middleware invoked\033[0m")

    await next(context)

    # Now inspect and potentially modify the result
    if context.result and function_name == "booking_tool":
        result_data = json.loads(context.result)

        # modify the original result if it is gold member
        if is_gold_member:
            result_data["priority_boarding"] = True
            result_data["priority_override"] = True
            context.result = json.dumps(result_data)


@executor(id="display_result")
async def display_result(
    response: AgentExecutorResponse, ctx: WorkflowContext[Never, str]
) -> None:
    await ctx.yield_output(response.agent_run_response.text)


booking_agent = AgentExecutor(
    chat_client.create_agent(
        instructions=(
            "You are a flight booking assistant that checks flight availability. "
            "Use the booking_tool tool to check if flights are available at the "
            "destination. "
            "Return JSON with fields: destination (string), is_available (bool), "
            "message (string), and priority_override (bool, true if "
            "priority member got special access). "
            "The message should summarize the availability status and mention "
            "if priority override occurred."
        ),
        tools=[booking_tool],
        response_format=BookingResult,
        middleware=[priority_check_middleware],  # MIDDLEWARE INJECTION
    ),
    id="booking_agent",
)


async def main() -> None:
    # Build the simple workflow
    workflow = (
        WorkflowBuilder()
        .set_start_executor(booking_agent)
        .add_edge(booking_agent, display_result)
        .build()
    )

    request = AgentExecutorRequest(
        messages=[ChatMessage(Role.USER, text="I want to book a flight to Paris")],
        should_respond=True,
    )

    # execute the workflow
    events = await workflow.run(request)

    # print the booking result
    outputs = events.get_outputs()
    print()
    print("Flight Booking Result:")
    print(BookingResult.model_validate_json(outputs[0]))
    print()


if __name__ == "__main__":
    asyncio.run(main())
