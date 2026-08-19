from typing import Literal

from pydantic import BaseModel


class TicketAnalysis(BaseModel):

    category: str

    intent: str

    priority: Literal[
        "low",
        "medium",
        "high",
        "urgent",
    ]


class AgentDecision(BaseModel):

    decision: Literal[
        "resolve",
        "escalate",
    ]

    reason: str