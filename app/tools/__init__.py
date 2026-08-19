from app.tools.customer_tools import (
    get_customer,
    get_customer_history,
)
from app.tools.knowledge_tools import (
    search_knowledge_base,
)
from app.tools.order_tools import (
    get_order,
)
from app.tools.payment_tools import (
    get_payment_status,
)
from app.tools.ticket_tools import (
    get_previous_tickets,
    get_ticket,
)

SUPPORT_TOOLS = [
    get_customer,
    get_customer_history,
    get_order,
    get_payment_status,
    get_ticket,
    get_previous_tickets,
    search_knowledge_base,
]


__all__ = [
    "SUPPORT_TOOLS",
    "get_customer",
    "get_customer_history",
    "get_order",
    "get_payment_status",
    "get_previous_tickets",
    "get_ticket",
    "search_knowledge_base",
]