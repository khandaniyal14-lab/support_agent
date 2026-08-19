import json
from datetime import UTC, datetime
from typing import Any

from sqlalchemy.orm import Session

from app.models.tool_approval import (
    ToolApproval,
)


class ToolApprovalService:

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.db = db

    def create_request(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> ToolApproval:

        approval = ToolApproval(
            tool_name=tool_name,
            arguments=json.dumps(
                arguments
            ),
            approved=False,
        )

        self.db.add(approval)
        self.db.commit()
        self.db.refresh(approval)

        return approval

    def approve(
        self,
        approval_id: int,
        approved_by: str,
    ) -> ToolApproval:

        approval = (
            self.db.get(
                ToolApproval,
                approval_id,
            )
        )

        if approval is None:
            raise ValueError(
                "Approval request not found."
            )

        if approval.approved:
            raise ValueError(
                "Approval request already approved."
            )

        approval.approved = True
        approval.approved_by = approved_by
        approval.approved_at = datetime.now(UTC)

        self.db.commit()
        self.db.refresh(approval)

        return approval

    def is_approved(
        self,
        approval_id: int,
    ) -> bool:

        approval = (
            self.db.get(
                ToolApproval,
                approval_id,
            )
        )

        if approval is None:
            return False

        return approval.approved