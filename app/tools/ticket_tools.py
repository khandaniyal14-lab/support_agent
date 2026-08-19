from langchain_core.tools import tool


@tool
def get_ticket(ticket_id: int) -> dict:
    """
    Get support ticket information using a ticket ID.
    """

    tickets = {
        1: {
            "id": 1,
            "customer_id": 1,
            "order_id": 1001,
            "subject": "Payment deducted but order cancelled",
            "description": (
                "My payment was deducted but my order "
                "was cancelled. What will happen to my money?"
            ),
            "category": "billing",
            "priority": "high",
            "status": "open",
        },
        2: {
            "id": 2,
            "customer_id": 2,
            "order_id": 1002,
            "subject": "Can I cancel my shipped order?",
            "description": (
                "My order has already shipped. "
                "Can I cancel it?"
            ),
            "category": "shipping",
            "priority": "medium",
            "status": "open",
        },
        3: {
            "id": 3,
            "customer_id": 3,
            "order_id": 1003,
            "subject": "Payment failed",
            "description": (
                "My payment failed when I tried "
                "to place my order."
            ),
            "category": "billing",
            "priority": "medium",
            "status": "open",
        },
    }

    ticket = tickets.get(ticket_id)

    if ticket is None:
        return {
            "found": False,
            "ticket_id": ticket_id,
        }

    return {
        "found": True,
        "ticket": ticket,
    }


@tool
def get_previous_tickets(
    customer_id: int,
) -> dict:
    """
    Get previous support tickets for a customer.
    """

    tickets = {
        1: [
            {
                "ticket_id": 101,
                "category": "billing",
                "summary": "Duplicate payment question",
                "resolution": (
                    "Payment records were verified."
                ),
            },
            {
                "ticket_id": 102,
                "category": "shipping",
                "summary": "Delayed delivery",
                "resolution": (
                    "Tracking information was provided."
                ),
            },
        ],
        2: [
            {
                "ticket_id": 103,
                "category": "account",
                "summary": "Password reset",
                "resolution": (
                    "Password reset instructions provided."
                ),
            }
        ],
        3: [],
    }

    return {
        "customer_id": customer_id,
        "tickets": tickets.get(
            customer_id,
            [],
        ),
    }