from pydantic import BaseModel, Field, field_validator


class QuestionResponse(BaseModel):
    user_question: str = Field(
        ..., description="The original question asked by the user."
    )

    response: str = Field(
        ..., description="A detailed and professional answer to the user's question."
    )

    @field_validator("response")
    def validate_response(cls, v: str) -> str:
        if not v or len(v.strip()) == 0:
            raise ValueError("Response must be a non-empty string.")
        return v

    @field_validator("user_question")
    def validate_user_question(cls, v: str) -> str:
        if not v or len(v.strip()) == 0:
            raise ValueError("User question must be a non-empty string.")
        return v
