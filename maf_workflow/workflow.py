from typing import Any

from agent_framework import (
    AgentExecutorRequest,
    AgentExecutorResponse,
    ChatMessage,
    Role,
    Workflow,
    WorkflowBuilder,
)

from maf_workflow.agents.customer_agent import create as create_customer_agent
from maf_workflow.agents.intent_detection_agent import (
    create_agent as create_intent_detection_agent,
)
from maf_workflow.executors import (
    handle_greeting,
    handle_inappropriate,
    handle_question_response,
    handle_statement,
    to_assistant_request,
)
from maf_workflow.hosting import container
from maf_workflow.models.intent_detection_result import IntentDetectionResult
from maf_workflow.protocols.i_azure_open_ai_chat_client_service import (
    IAzureOpenAIChatClientService,
)


def get_condition(field: str):
    def condition(message: Any) -> bool:
        if not isinstance(message, AgentExecutorResponse):
            return True

        try:
            detection = IntentDetectionResult.model_validate_json(
                message.agent_run_response.text
            )
            result = getattr(detection, field) is True
            print(f"\033[92mCondition check on field '{field}': {result}\033[0m")
            return result
        except Exception:
            return False

    return condition


def create() -> Workflow:
    chat_client = container[IAzureOpenAIChatClientService].get_client()
    intent_detection_agent = create_intent_detection_agent(chat_client)
    customer_assistant_agent = create_customer_agent(chat_client)

    return (
        WorkflowBuilder()
        .set_start_executor(intent_detection_agent)
        .add_edge(
            intent_detection_agent,
            to_assistant_request,
            condition=get_condition("is_question"),
        )
        .add_edge(to_assistant_request, customer_assistant_agent)
        .add_edge(customer_assistant_agent, handle_question_response)
        .add_edge(
            intent_detection_agent,
            handle_greeting,
            condition=get_condition("is_greeting"),
        )
        .add_edge(
            intent_detection_agent,
            handle_inappropriate,
            condition=get_condition("is_inappropriate"),
        )
        .add_edge(
            intent_detection_agent,
            handle_statement,
            condition=get_condition("is_statement"),
        )
        .build()
    )


async def execute_workflow(text: str) -> None:
    print()
    workflow = create()
    request = AgentExecutorRequest(
        messages=[ChatMessage(Role.USER, text=text)], should_respond=True
    )
    events = await workflow.run(request)
    outputs = events.get_outputs()
    if outputs:
        print()
        print(f"\033[1mWorkflow output: {outputs[0]}\033[0m")
