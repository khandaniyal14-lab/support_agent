from langchain_core.tools import tool


@tool
def get_customer(customer_id: int) -> dict:
    """
    Get customer information using the customer ID.

    Use this tool when customer information is required
    to investigate a support ticket.
    """

    customers = {
        1: {
            "id": 1,
            "name": "John Smith",
            "email": "john@example.com",
            "status": "active",
        },
        2: {
            "id": 2,
            "name": "Sarah Johnson",
            "email": "sarah@example.com",
            "status": "active",
        },
        3: {
            "id": 3,
            "name": "Michael Brown",
            "email": "michael@example.com",
            "status": "active",
        },
    }

    customer = customers.get(customer_id)

    if customer is None:
        return {
            "found": False,
            "customer_id": customer_id,
        }

    return {
        "found": True,
        "customer": customer,
    }


@tool
def get_customer_history(
    customer_id: int,
) -> dict:
    """
    Get previous support activity for a customer.

    Use this tool when previous customer interactions
    may help resolve the current issue.
    """

    history = {
        1: [
            {
                "ticket_id": 101,
                "category": "billing",
                "status": "resolved",
                "summary": "Customer asked about a duplicate payment.",
            },
            {
                "ticket_id": 102,
                "category": "shipping",
                "status": "resolved",
                "summary": "Customer asked about delayed delivery.",
            },
        ],
        2: [
            {
                "ticket_id": 103,
                "category": "account",
                "status": "resolved",
                "summary": "Customer requested password reset.",
            }
        ],
        3: [],
    }

    return {
        "customer_id": customer_id,
        "tickets": history.get(
            customer_id,
            [],
        ),
    }