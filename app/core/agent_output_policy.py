from app.schemas.agent_output import (
    AgentResponse,
)


class AgentOutputPolicyError(
    ValueError
):
    pass


def validate_agent_response_policy(
    response: AgentResponse,
) -> AgentResponse:

    if (
        response.requires_escalation
        and response.priority == "low"
    ):
        raise AgentOutputPolicyError(
            "Escalated tickets cannot have low priority."
        )

    if response.confidence < 0.5:
        response.requires_escalation = True

    return response