from typing import Literal

from app.agents.graph.state import SupportState


def route_decision(
    state: SupportState,
) -> Literal[
    "resolve",
    "escalate",
]:

    decision = state.get(
        "decision"
    )

    if decision == "resolve":
        return "resolve"

    return "escalate"