import pytest
from pydantic import ValidationError

from app.ai.schemas import TicketClassification


def test_valid_classification():
    result = TicketClassification(
        category="billing",
        intent="duplicate charge",
        priority="high",
        sentiment="negative",
        confidence=0.95,
        reasoning="The customer reports being charged twice.",
    )

    assert result.category == "billing"
    assert result.priority == "high"
    assert result.confidence == 0.95


def test_confidence_must_be_between_zero_and_one():
    with pytest.raises(ValidationError):
        TicketClassification(
            category="billing",
            intent="duplicate charge",
            priority="high",
            sentiment="negative",
            confidence=1.5,
            reasoning="Invalid confidence.",
        )


def test_invalid_category():
    with pytest.raises(ValidationError):
        TicketClassification(
            category="invalid",
            intent="test",
            priority="low",
            sentiment="neutral",
            confidence=0.5,
            reasoning="Invalid category.",
        )