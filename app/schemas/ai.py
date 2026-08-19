from pydantic import BaseModel, Field


class AnalyzeTicketRequest(BaseModel):
    ticket: str = Field(
        min_length=1,
        max_length=10000,
    )