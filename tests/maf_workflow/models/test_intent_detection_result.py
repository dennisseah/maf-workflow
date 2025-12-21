from typing import Any

import pytest

from maf_workflow.models.intent_detection_result import IntentDetectionResult


@pytest.mark.parametrize(
    "flag",
    [
        "is_greeting",
        "is_inappropriate",
        "is_question",
        "is_statement",
    ],
)
def test_intent_detection_result_validation(flag: str):
    # Test valid case for is_greeting
    _params: dict[str, Any] = {
        "is_greeting": False,
        "is_inappropriate": False,
        "is_question": False,
        "is_statement": False,
        "message_content": "Hello there!",
        "response": "Hi! How can I assist you today?",
    }
    _params[flag] = True
    IntentDetectionResult(**_params)


def test_intent_detection_result_validation_err():
    _params: dict[str, Any] = {
        "is_greeting": False,
        "is_inappropriate": True,
        "is_question": True,
        "is_statement": False,
        "message_content": "Hello there!",
        "response": "Hi! How can I assist you today?",
    }
    with pytest.raises(ValueError):
        IntentDetectionResult(**_params)
