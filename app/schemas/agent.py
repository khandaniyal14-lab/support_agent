from pydantic import BaseModel, Field


class AgentRequest(BaseModel):

    request: str = Field(
        min_length=1,
        max_length=10000,
    )

    conversation_id: str = Field(
        default="default",
        min_length=1,
        max_length=100,
    )

    ticket_id: int | None = None


class AgentResponse(BaseModel):

    request: str
    conversation_id: str
    response: str