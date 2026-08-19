import pytest

from app.core.tool_authorization import (
    ToolAuthorization,
    ToolAuthorizationError,
)
from app.core.tool_guard import ToolGuard
from app.core.tool_permissions import (
    ToolPermission,
)


def test_read_tool_is_allowed():

    authorization = ToolAuthorization()

    authorization.authorize(
        "get_customer"
    )


def test_write_tool_requires_authorization():

    authorization = ToolAuthorization()

    with pytest.raises(
        ToolAuthorizationError
    ):
        authorization.authorize(
            "create_refund_request"
        )


def test_write_tool_can_be_authorized():

    authorization = ToolAuthorization()

    authorization.authorize(
        "create_refund_request",
        approved=True,
    )


def test_unknown_tool_is_rejected():

    authorization = ToolAuthorization()

    with pytest.raises(
        ToolAuthorizationError
    ):
        authorization.authorize(
            "delete_database"
        )


def test_read_permission():

    authorization = ToolAuthorization()

    permission = authorization.get_permission(
        "get_order"
    )

    assert permission == ToolPermission.READ


def test_write_permission():

    authorization = ToolAuthorization()

    permission = authorization.get_permission(
        "create_refund_request"
    )

    assert permission == ToolPermission.WRITE





def test_read_tool_executes():

    guard = ToolGuard()

    def get_customer(
        customer_id: str,
    ) -> dict:

        return {
            "id": customer_id,
            "name": "Test Customer",
        }

    result = guard.execute(
        "get_customer",
        get_customer,
        customer_id="customer-1001",
    )

    assert result["id"] == "customer-1001"


def test_write_tool_cannot_execute_without_approval():

    guard = ToolGuard()

    def create_refund_request(
        order_id: int,
    ) -> dict:

        return {
            "status": "created",
            "order_id": order_id,
        }

    with pytest.raises(
        ToolAuthorizationError
    ):
        guard.execute(
            "create_refund_request",
            create_refund_request,
            order_id=1001,
        )


def test_write_tool_executes_with_approval():

    guard = ToolGuard()

    def create_refund_request(
        order_id: int,
    ) -> dict:

        return {
            "status": "created",
            "order_id": order_id,
        }

    result = guard.execute(
        "create_refund_request",
        create_refund_request,
        approved=True,
        order_id=1001,
    )

    assert result["status"] == "created"




def test_refund_requires_approval():

    guard = ToolGuard()

    def create_refund_request(
        order_id: int,
    ) -> dict:

        return {
            "order_id": order_id,
            "status": "created",
        }

    with pytest.raises(
        PermissionError
    ):
        guard.execute(
            "create_refund_request",
            create_refund_request,
            order_id=1001,
        )


def test_refund_executes_after_approval():

    guard = ToolGuard()

    def create_refund_request(
        order_id: int,
    ) -> dict:

        return {
            "order_id": order_id,
            "status": "created",
        }

    result = guard.execute(
        "create_refund_request",
        create_refund_request,
        approved=True,
        order_id=1001,
    )

    assert result["status"] == "created"