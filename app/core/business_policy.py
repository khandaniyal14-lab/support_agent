from dataclasses import dataclass
from typing import Any


class PolicyViolation(
    ValueError
):
    pass


@dataclass(frozen=True)
class PolicyResult:
    allowed: bool
    requires_approval: bool
    reason: str


class BusinessPolicy:

    def check(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> PolicyResult:

        if tool_name == "create_refund_request":
            return self._check_refund(
                arguments
            )

        if tool_name == "escalate_ticket":
            return self._check_escalation(
                arguments
            )

        if tool_name == "send_customer_response":
            return self._check_customer_response(
                arguments
            )

        return PolicyResult(
            allowed=True,
            requires_approval=False,
            reason="Read operation.",
        )

    def _check_refund(
        self,
        arguments: dict[str, Any],
    ) -> PolicyResult:

        order_id = arguments.get(
            "order_id"
        )

        if order_id is None:
            raise PolicyViolation(
                "order_id is required for refund."
            )

        return PolicyResult(
            allowed=True,
            requires_approval=True,
            reason=(
                "Refund requests require "
                "human approval."
            ),
        )

    def _check_escalation(
        self,
        arguments: dict[str, Any],
    ) -> PolicyResult:

        ticket_id = arguments.get(
            "ticket_id"
        )

        if ticket_id is None:
            raise PolicyViolation(
                "ticket_id is required "
                "for escalation."
            )

        return PolicyResult(
            allowed=True,
            requires_approval=True,
            reason=(
                "Ticket escalation requires "
                "human approval."
            ),
        )

    def _check_customer_response(
        self,
        arguments: dict[str, Any],
    ) -> PolicyResult:

        message = arguments.get(
            "message"
        )

        if not message:
            raise PolicyViolation(
                "Customer message is required."
            )

        if len(message) > 5000:
            raise PolicyViolation(
                "Customer message is too long."
            )

        return PolicyResult(
            allowed=True,
            requires_approval=True,
            reason=(
                "Customer communication requires "
                "human approval."
            ),
        )