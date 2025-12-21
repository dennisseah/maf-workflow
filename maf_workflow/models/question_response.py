from pydantic import BaseModel


class QuestionResponse(BaseModel):
    user_question: str
    response: str
