import json
from typing import Any

from pydantic import ValidationError

from app.core.validation import (
    validate_output,
)
from app.schemas.agent_output import (
    AgentResponse,
    ToolCallRequest,
)


class OutputValidationError(
    ValueError
):
    pass


def validate_agent_output(
    raw_output: str,
) -> AgentResponse:

    try:
        raw_output = validate_output(
            raw_output
        )

    except ValueError as exc:
        raise OutputValidationError(
            str(exc)
        ) from exc

    try:
        data: Any = json.loads(
            raw_output
        )

    except json.JSONDecodeError as exc:
        raise OutputValidationError(
            "LLM returned invalid JSON."
        ) from exc

    try:
        return AgentResponse.model_validate(
            data
        )

    except ValidationError as exc:
        raise OutputValidationError(
            "LLM output failed schema validation."
        ) from exc


def validate_tool_call(
    raw_output: str,
) -> ToolCallRequest:

    try:
        raw_output = validate_output(
            raw_output
        )

    except ValueError as exc:
        raise OutputValidationError(
            str(exc)
        ) from exc

    try:
        data: Any = json.loads(
            raw_output
        )

    except json.JSONDecodeError as exc:
        raise OutputValidationError(
            "Tool call output is not valid JSON."
        ) from exc

    try:
        return ToolCallRequest.model_validate(
            data
        )

    except ValidationError as exc:
        raise OutputValidationError(
            "Tool call failed schema validation."
        ) from exc