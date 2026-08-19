import pytest

from app.core.business_policy import (
    BusinessPolicy,
    PolicyViolation,
)


def test_refund_requires_order_id():

    policy = BusinessPolicy()

    with pytest.raises(
        PolicyViolation
    ):
        policy.check(
            "create_refund_request",
            {},
        )


def test_refund_requires_approval():

    policy = BusinessPolicy()

    result = policy.check(
        "create_refund_request",
        {
            "order_id": 1001,
        },
    )

    assert result.allowed is True
    assert result.requires_approval is True


def test_escalation_requires_ticket_id():

    policy = BusinessPolicy()

    with pytest.raises(
        PolicyViolation
    ):
        policy.check(
            "escalate_ticket",
            {},
        )


def test_customer_message_required():

    policy = BusinessPolicy()

    with pytest.raises(
        PolicyViolation
    ):
        policy.check(
            "send_customer_response",
            {},
        )


def test_customer_message_length():

    policy = BusinessPolicy()

    with pytest.raises(
        PolicyViolation
    ):
        policy.check(
            "send_customer_response",
            {
                "message": "A" * 5001,
            },
        )


def test_read_operation():

    policy = BusinessPolicy()

    result = policy.check(
        "get_order",
        {
            "order_id": 1001,
        },
    )

    assert result.allowed is True
    assert result.requires_approval is False