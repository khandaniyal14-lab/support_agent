import json

import pytest

from app.core.agent_output_policy import (
    AgentOutputPolicyError,
    validate_agent_response_policy,
)
from app.core.output_validation import (
    OutputValidationError,
    validate_agent_output,
    validate_tool_call,
)


def test_valid_agent_output():

    raw_output = json.dumps(
        {
            "response": (
                "Your payment was unsuccessful."
            ),
            "category": "billing",
            "priority": "high",
            "requires_escalation": False,
            "confidence": 0.95,
        }
    )

    result = validate_agent_output(
        raw_output
    )

    assert result.category == "billing"
    assert result.priority == "high"
    assert result.confidence == 0.95


def test_invalid_json():

    with pytest.raises(
        OutputValidationError
    ):
        validate_agent_output(
            "this is not json"
        )


def test_missing_field():

    raw_output = json.dumps(
        {
            "response": "Test",
            "category": "billing",
            "priority": "high",
        }
    )

    with pytest.raises(
        OutputValidationError
    ):
        validate_agent_output(
            raw_output
        )


def test_invalid_priority():

    raw_output = json.dumps(
        {
            "response": "Test",
            "category": "billing",
            "priority": "extreme",
            "requires_escalation": False,
            "confidence": 0.9,
        }
    )

    with pytest.raises(
        OutputValidationError
    ):
        validate_agent_output(
            raw_output
        )


def test_invalid_confidence():

    raw_output = json.dumps(
        {
            "response": "Test",
            "category": "billing",
            "priority": "high",
            "requires_escalation": False,
            "confidence": 2.0,
        }
    )

    with pytest.raises(
        OutputValidationError
    ):
        validate_agent_output(
            raw_output
        )


def test_low_confidence_forces_escalation():

    raw_output = json.dumps(
        {
            "response": "I am not certain.",
            "category": "billing",
            "priority": "high",
            "requires_escalation": False,
            "confidence": 0.3,
        }
    )

    result = validate_agent_output(
        raw_output
    )

    result = validate_agent_response_policy(
        result
    )

    assert result.requires_escalation is True


def test_invalid_escalation_policy():

    raw_output = json.dumps(
        {
            "response": "Test",
            "category": "billing",
            "priority": "low",
            "requires_escalation": True,
            "confidence": 0.9,
        }
    )

    result = validate_agent_output(
        raw_output
    )

    with pytest.raises(
        AgentOutputPolicyError
    ):
        validate_agent_response_policy(
            result
        )


def test_valid_tool_call():

    raw_output = json.dumps(
        {
            "tool_name": "get_order",
            "arguments": {
                "order_id": 1001,
            },
        }
    )

    result = validate_tool_call(
        raw_output
    )

    assert result.tool_name == "get_order"
    assert result.arguments["order_id"] == 1001


def test_invalid_tool_call():

    raw_output = json.dumps(
        {
            "arguments": {},
        }
    )

    with pytest.raises(
        OutputValidationError
    ):
        validate_tool_call(
            raw_output
        )