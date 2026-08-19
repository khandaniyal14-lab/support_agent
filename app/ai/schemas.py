from typing import Literal

from pydantic import BaseModel, Field

TicketCategory = Literal[
    "billing",
    "technical",
    "account",
    "shipping",
    "product",
    "refund",
    "cancellation",
    "other",
]


TicketPriority = Literal[
    "low",
    "medium",
    "high",
    "urgent",
]


TicketSentiment = Literal[
    "positive",
    "neutral",
    "negative",
]


class TicketClassification(BaseModel):
    category: TicketCategory = Field(
        description="The main category of the customer support ticket."
    )

    intent: str = Field(
        min_length=1,
        max_length=200,
        description="The specific customer intent."
    )

    priority: TicketPriority = Field(
        description="The urgency of the ticket."
    )

    sentiment: TicketSentiment = Field(
        description="The customer's sentiment."
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Model confidence between 0 and 1."
    )

    reasoning: str = Field(
        min_length=1,
        max_length=1000,
        description="Short explanation supporting the classification."
    )