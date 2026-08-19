from enum import Enum


class ToolPermission(str, Enum):
    READ = "read"
    WRITE = "write"


TOOL_PERMISSIONS: dict[str, ToolPermission] = {
    # READ
    "get_customer": ToolPermission.READ,
    "get_customer_history": ToolPermission.READ,
    "get_order": ToolPermission.READ,
    "get_payment_status": ToolPermission.READ,
    "get_ticket": ToolPermission.READ,
    "get_previous_tickets": ToolPermission.READ,
    "search_knowledge_base": ToolPermission.READ,
    "check_refund_status": ToolPermission.READ,

    # WRITE
    "create_refund_request": ToolPermission.WRITE,
    "escalate_ticket": ToolPermission.WRITE,
    "send_customer_response": ToolPermission.WRITE,
}