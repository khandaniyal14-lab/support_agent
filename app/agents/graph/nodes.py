import json
from typing import Any

from app.agents.graph.schemas import (
    AgentDecision,
    TicketAnalysis,
)
from app.agents.graph.state import SupportState
from app.agents.prompt import (
    CLASSIFICATION_PROMPT,
    DECISION_PROMPT,
)
from app.ai.llm import LLMService
from app.core.tool_guard import ToolGuard
from app.rag.retrieval import Retriever
from app.tools import (
    get_customer,
    get_customer_history,
    get_order,
    get_payment_status,
    get_previous_tickets,
    get_ticket,
    search_knowledge_base,
)


class SupportGraphNodes:

    def __init__(
        self,
        llm_service: LLMService | None = None,
        retriever: Retriever | None = None,
    ) -> None:

        self.llm = (
            llm_service
            or LLMService()
        )

        self.retriever = (
            retriever
            or Retriever()
        )

        self.tool_guard = ToolGuard()

    def classify(
        self,
        state: SupportState,
    ) -> dict[str, Any]:

        messages = state["messages"]

        user_message = messages[-1].content

        response = self.llm.generate_structured(
            system_prompt=CLASSIFICATION_PROMPT,
            user_prompt=user_message,
            response_format={
                "type": "json_object",
            },
        )

        analysis = TicketAnalysis.model_validate(
            json.loads(response)
        )

        return {
            "category": analysis.category,
            "intent": analysis.intent,
            "priority": analysis.priority,
        }

    def retrieve(
        self,
        state: SupportState,
    ) -> dict[str, Any]:

        messages = state["messages"]

        user_message = messages[-1].content

        results = self.retriever.search(
            query=user_message,
            top_k=5,
        )

        documents = [
            {
                "source": result.source,
                "category": result.category,
                "content": result.content,
                "score": result.score,
            }
            for result in results
        ]

        return {
            "retrieved_documents": documents,
        }

    def investigate(
        self,
        state: SupportState,
    ) -> dict[str, Any]:

        messages = state["messages"]

        user_message = messages[-1].content

        tool_results: list[dict[str, Any]] = []

        ticket_id = state.get(
            "ticket_id"
        )

        customer_id = state.get(
            "customer_id"
        )

        order_id = state.get(
            "order_id"
        )

        if ticket_id is not None:

            ticket_result = self.tool_guard.execute(
                "get_ticket",
                get_ticket,
                approved=False,
                ticket_id=ticket_id,
            )

            tool_results.append(
                {
                    "tool": "get_ticket",
                    "result": ticket_result,
                }
            )

            ticket = ticket_result.get(
                "ticket"
            )

            if ticket:

                customer_id = ticket.get(
                    "customer_id"
                )

                order_id = ticket.get(
                    "order_id"
                )

        if customer_id is not None:

            customer_result = self.tool_guard.execute(
                "get_customer",
                get_customer,
                approved=False,
                customer_id=customer_id,
            )

            tool_results.append(
                {
                    "tool": "get_customer",
                    "result": customer_result,
                }
            )

            history_result = (
                get_customer_history.invoke(
                    {
                        "customer_id": customer_id,
                    }
                )
            )

            tool_results.append(
                {
                    "tool": "get_customer_history",
                    "result": history_result,
                }
            )

            previous_result = (
                get_previous_tickets.invoke(
                    {
                        "customer_id": customer_id,
                    }
                )
            )

            tool_results.append(
                {
                    "tool": "get_previous_tickets",
                    "result": previous_result,
                }
            )

        if order_id is not None:

            order_result = self.tool_guard.execute(
                "get_order",
                get_order,
                approved=False,
                order_id=order_id,
            )

            tool_results.append(
                {
                    "tool": "get_order",
                    "result": order_result,
                }
            )

            payment_result = (
                get_payment_status.invoke(
                    {
                        "order_id": order_id,
                    }
                )
            )

            tool_results.append(
                {
                    "tool": "get_payment_status",
                    "result": payment_result,
                }
            )

        knowledge_result = (
            self.tool_guard.execute(
                "search_knowledge_base",
                search_knowledge_base,
                approved=False,
                query=user_message,
            )
        )

        tool_results.append(
            {
                "tool": "search_knowledge_base",
                "result": knowledge_result,
            }
        )

        return {
            "customer_id": customer_id,
            "order_id": order_id,
            "tool_results": tool_results,
        }

    def decide(
        self,
        state: SupportState,
    ) -> dict[str, Any]:

        investigation = {
            "documents": state.get(
                "retrieved_documents",
                [],
            ),
            "tools": state.get(
                "tool_results",
                [],
            ),
        }

        response = self.llm.generate_structured(
            system_prompt=DECISION_PROMPT,
            user_prompt=json.dumps(
                investigation,
                default=str,
            ),
            response_format={
                "type": "json_object",
            },
        )

        decision = AgentDecision.model_validate(
            json.loads(response)
        )

        return {
            "decision": decision.decision,
            "resolution": decision.reason,
        }

    def respond(
        self,
        state: SupportState,
    ) -> dict[str, Any]:

        messages = state["messages"]

        user_request = messages[-1].content

        context = {
            "classification": {
                "category": state.get(
                    "category"
                ),
                "intent": state.get(
                    "intent"
                ),
                "priority": state.get(
                    "priority"
                ),
            },
            "documents": state.get(
                "retrieved_documents",
                [],
            ),
            "tools": state.get(
                "tool_results",
                [],
            ),
            "decision": state.get(
                "decision"
            ),
            "resolution": state.get(
                "resolution"
            ),
        }

        system_prompt = """
You are the final customer support response generator.

Use only the verified information provided in the
investigation context.

Never invent information.

Never claim that a write operation was completed.

If the decision is "escalate", clearly explain that
the case requires human support.

Keep the response concise and useful.
"""

        response = self.llm.generate_structured(
            system_prompt=system_prompt,
            user_prompt=(
                f"Customer request:\n"
                f"{user_request}\n\n"
                f"Investigation:\n"
                f"{json.dumps(context, default=str)}"
            ),
            response_format={
                "type": "json_object",
            },
        )

        data = json.loads(response)

        final_response = data.get(
            "response"
        )

        if not final_response:
            final_response = (
                state.get("resolution")
                or "The case requires further investigation."
            )

        return {
            "final_response": final_response,
        }

    def escalate(
        self,
        state: SupportState,
    ) -> dict[str, Any]:

        return {
            "final_response": (
                "This case requires human support "
                "because it cannot be safely resolved "
                "automatically."
            ),
        }