from typing import Annotated, Any, Literal

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class SupportState(TypedDict, total=False):

    messages: Annotated[
        list[BaseMessage],
        add_messages,
    ]

    ticket_id: int | None

    customer_id: int | None

    order_id: int | None

    category: str | None

    priority: str | None

    intent: str | None

    retrieved_documents: list[dict[str, Any]]

    tool_results: list[dict[str, Any]]

    decision: Literal[
        "resolve",
        "escalate",
    ] | None

    resolution: str | None

    final_response: str | None

    error: str | None