from langchain_core.tools import tool


@tool
def get_payment_status(
    order_id: int,
) -> dict:
    """
    Get payment information associated with an order.

    Use this tool when a customer reports a payment,
    duplicate charge, failed payment, refund, or
    payment-status problem.
    """

    payments = {
        1001: {
            "order_id": 1001,
            "status": "completed",
            "amount": 299.99,
            "currency": "USD",
            "transaction_count": 1,
        },
        1002: {
            "order_id": 1002,
            "status": "completed",
            "amount": 149.99,
            "currency": "USD",
            "transaction_count": 1,
        },
        1003: {
            "order_id": 1003,
            "status": "pending",
            "amount": 89.99,
            "currency": "USD",
            "transaction_count": 1,
        },
    }

    payment = payments.get(order_id)

    if payment is None:
        return {
            "found": False,
            "order_id": order_id,
        }

    return {
        "found": True,
        "payment": payment,
    }