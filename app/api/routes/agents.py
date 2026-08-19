from fastapi import APIRouter, HTTPException

from app.agents.support_agent import (
    SupportAgent,
)
from app.schemas.agent import (
    AgentRequest,
    AgentResponse,
)

router = APIRouter(
    prefix="/agent",
    tags=["Agent"],
)


agent = SupportAgent()


@router.post(
    "/run",
    response_model=AgentResponse,
)
def run_agent(
    request: AgentRequest,
) -> AgentResponse:

    try:

        response = agent.run(
            request=request.request,
            conversation_id=(
                request.conversation_id
            ),
            ticket_id=request.ticket_id,
        )

        return AgentResponse(
            request=request.request,
            conversation_id=(
                request.conversation_id
            ),
            response=response,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail="Agent execution failed.",
        ) from exc