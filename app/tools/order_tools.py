from langchain_core.tools import tool


@tool
def get_order(order_id: int) -> dict:
    """
    Get order information using an order ID.

    Use this tool when the support request involves
    order status, cancellation, shipping, or refunds.
    """

    orders = {
        1001: {
            "id": 1001,
            "customer_id": 1,
            "status": "cancelled",
            "total_amount": 299.99,
            "currency": "USD",
            "payment_status": "paid",
        },
        1002: {
            "id": 1002,
            "customer_id": 2,
            "status": "shipped",
            "total_amount": 149.99,
            "currency": "USD",
            "payment_status": "paid",
        },
        1003: {
            "id": 1003,
            "customer_id": 3,
            "status": "processing",
            "total_amount": 89.99,
            "currency": "USD",
            "payment_status": "pending",
        },
    }

    order = orders.get(order_id)

    if order is None:
        return {
            "found": False,
            "order_id": order_id,
        }

    return {
        "found": True,
        "order": order,
    }