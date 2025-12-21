from agent_framework import (
    AgentExecutorRequest,
    AgentExecutorResponse,
    ChatMessage,
    Role,
    WorkflowContext,
    executor,
)
from typing_extensions import Never

from maf_workflow.models.intent_detection_result import IntentDetectionResult
from maf_workflow.models.question_response import QuestionResponse


@executor(id="handle_greeting")
async def handle_greeting(
    response: AgentExecutorResponse, ctx: WorkflowContext[Never, str]
) -> None:
    # just return the greeting response from the intent detection agent
    intent = IntentDetectionResult.model_validate_json(response.agent_run_response.text)
    if intent.is_greeting:
        await ctx.yield_output(intent.response)
    else:
        raise RuntimeError("This executor should not be called.")


@executor(id="handle_inappropriate")
async def handle_inappropriate(
    response: AgentExecutorResponse, ctx: WorkflowContext[Never, str]
) -> None:
    intent = IntentDetectionResult.model_validate_json(response.agent_run_response.text)
    if intent.is_inappropriate:
        await ctx.yield_output(
            "The message has been flagged as inappropriate and will not be processed."
        )
    else:
        raise RuntimeError("This executor should not be called.")


@executor(id="handle_statement")
async def handle_statement(
    response: AgentExecutorResponse, ctx: WorkflowContext[Never, str]
) -> None:
    intent = IntentDetectionResult.model_validate_json(response.agent_run_response.text)
    if intent.is_statement:
        await ctx.yield_output("I am at your service for any questions you may have.")
    else:
        raise RuntimeError("This executor should not be called.")


@executor(id="to_assistant_request")
async def to_assistant_request(
    response: AgentExecutorResponse, ctx: WorkflowContext[AgentExecutorRequest]
) -> None:
    intent = IntentDetectionResult.model_validate_json(response.agent_run_response.text)

    # Create a new request for the email assistant with the original email content
    request = AgentExecutorRequest(
        messages=[ChatMessage(Role.USER, text=intent.message_content)],
        should_respond=True,
    )
    await ctx.send_message(request)


@executor(id="question_response")
async def handle_question_response(
    response: AgentExecutorResponse, ctx: WorkflowContext[Never, str]
) -> None:
    qn_response = QuestionResponse.model_validate_json(response.agent_run_response.text)
    await ctx.yield_output(f"{qn_response.user_question}\n{qn_response.response}")
