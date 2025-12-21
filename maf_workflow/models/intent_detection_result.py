from pydantic import BaseModel, Field, model_validator


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

    @model_validator(mode="after")
    def validate_mutually_exclusive_intents(self) -> "IntentDetectionResult":
        """Validate that is_greeting, is_inappropriate, is_question, is_statement are
        mutually exclusive."""
        intents = [
            self.is_greeting,
            self.is_inappropriate,
            self.is_question,
            self.is_statement,
        ]
        true_count = sum(intents)

        if true_count != 1:
            raise ValueError(
                "Exactly one of is_greeting, is_inappropriate, is_question, or is_statement must be True. "  # noqa: E501
                f"Found {true_count} set to True."
            )

        return self
