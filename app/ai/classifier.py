import json

from pydantic import ValidationError

from app.ai.llm import LLMService
from app.ai.prompts import CLASSIFICATION_SYSTEM_PROMPT
from app.ai.schemas import TicketClassification


class TicketClassifier:
    def __init__(
        self,
        llm_service: LLMService | None = None,
    ) -> None:
        self.llm = llm_service or LLMService()

    def classify(
        self,
        ticket: str,
    ) -> TicketClassification:

        if not ticket.strip():
            raise ValueError(
                "Ticket cannot be empty."
            )

        user_prompt = f"""
Analyze the following customer support ticket.

TICKET:
{ticket}
"""

        response = self.llm.generate_structured(
            system_prompt=CLASSIFICATION_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            response_format={
                "type": "json_object"
            },
        )

        try:
            data = json.loads(response)

        except json.JSONDecodeError as exc:
            raise ValueError(
                "LLM returned invalid JSON."
            ) from exc

        try:
            return TicketClassification.model_validate(
                data
            )

        except ValidationError as exc:
            raise ValueError(
                "LLM response failed schema validation."
            ) from exc