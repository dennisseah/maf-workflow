import pytest

from maf_workflow.models.question_response import QuestionResponse


def test_question_response_validation():
    # Test valid case
    qr = QuestionResponse(
        user_question="What is the capital of France?",
        response="The capital of France is Paris.",
    )
    assert qr.user_question == "What is the capital of France?"
    assert qr.response == "The capital of France is Paris."


def test_question_response_validation_err():
    with pytest.raises(ValueError):
        QuestionResponse(
            user_question="What is the capital of France?",
            response="",
        )

    with pytest.raises(ValueError):
        QuestionResponse(
            user_question="",
            response="The capital of France is Paris.",
        )
