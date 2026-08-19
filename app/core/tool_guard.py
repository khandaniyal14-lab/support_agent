from collections.abc import Callable
from typing import Any

from app.core.business_policy import (
    BusinessPolicy,
)
from app.core.resilient import (
    execute_resilient,
)
from app.core.tool_authorization import (
    ToolAuthorization,
)


class ToolGuard:

    def __init__(
        self,
        authorization: ToolAuthorization | None = None,
        policy: BusinessPolicy | None = None,
    ) -> None:

        self.authorization = (
            authorization
            or ToolAuthorization()
        )

        self.policy = (
            policy
            or BusinessPolicy()
        )

    def execute(
        self,
        tool_name: str,
        tool: Callable[..., Any],
        *,
        approved: bool = False,
        **arguments: Any,
    ) -> Any:

        # -------------------------
        # Authorization
        # -------------------------

        self.authorization.authorize(
            tool_name=tool_name,
            approved=approved,
        )

        # -------------------------
        # Business Policy
        # -------------------------

        policy_result = self.policy.check(
            tool_name=tool_name,
            arguments=arguments,
        )

        if not policy_result.allowed:
            raise PermissionError(
                policy_result.reason
            )

        # -------------------------
        # Human Approval
        # -------------------------

        if (
            policy_result.requires_approval
            and not approved
        ):
            raise PermissionError(
                policy_result.reason
            )

        # -------------------------
        # Execute
        # -------------------------

        return execute_resilient(
            tool,
            **arguments,
        )