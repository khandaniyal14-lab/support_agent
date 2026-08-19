from typing import Literal

from pydantic import BaseModel, Field


class AgentResponse(BaseModel):
    response: str = Field(
        min_length=1,
        max_length=10_000,
    )

    category: str = Field(
        min_length=1,
        max_length=100,
    )

    priority: Literal[
        "low",
        "medium",
        "high",
        "critical",
    ]

    requires_escalation: bool

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )


class ToolCallRequest(BaseModel):
    tool_name: str = Field(
        min_length=1,
        max_length=100,
    )

    arguments: dict