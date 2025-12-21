from pydantic import BaseModel, Field


class IntentDetectionResult(BaseModel):
    message_content: str = Field(..., description="The original message content.")
    is_greeting: bool = Field(
        ..., description="True if the message is a greeting, false otherwise."
    )
    is_inappropriate: bool = Field(
        ..., description="True if the message is inappropriate, false otherwise."
    )
    is_question: bool = Field(
        ...,
        description="True if the message is a question or request for information, false otherwise.",  # noqa: E501
    )
    is_statement: bool = Field(
        ...,
        description="True if the message is a general statement, false otherwise.",
    )
    response: str = Field(
        ...,
        description="Generated response to the message if it is a greeting; empty string otherwise.",  # noqa: E501
    )
