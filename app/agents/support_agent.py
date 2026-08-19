from app.agents.graph.workflow import SupportWorkflow
from app.core.security_guard import (
    security_check,
)
from app.db.session import SessionLocal
from app.memory.service import ConversationMemoryService


class SupportAgent:

    def __init__(
        self,
        workflow: SupportWorkflow | None = None,
    ) -> None:

        self.workflow = (
            workflow
            or SupportWorkflow()
        )

        

    def run(
        self,
        request: str,
        conversation_id: str = "default",
        ticket_id: int | None = None,
    ) -> str:

        request = security_check(request)

        db = SessionLocal()

        try:

            memory = ConversationMemoryService(db)

            memory.add_user_message(
                conversation_id=conversation_id,
                content=request,
            )

            history = memory.get_history(
                conversation_id=conversation_id,
            )

            context = "\n".join(
                f"{message['role']}: "
                f"{message['content']}"
                for message in history
            )

            graph = self.workflow.compile()

            config = {
                "configurable": {
                    "thread_id": conversation_id,
                }
            }

            result = graph.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": context,
                        }
                    ],
                    "ticket_id": ticket_id,
                    "customer_id": None,
                    "order_id": None,
                    "category": None,
                    "priority": None,
                    "intent": None,
                    "retrieved_documents": [],
                    "tool_results": [],
                    "decision": None,
                    "resolution": None,
                    "final_response": None,
                    "error": None,
                },
                config=config,
            )

            response = result.get("final_response")

            if not response:
                response = (
                    "Unable to generate a support response."
                )

            # Convert structured LLM response to text
            if isinstance(response, dict):
                response = response.get("text")

            if not response:
                response = (
                    "Unable to generate a support response."
                )

            response = str(response)

            memory.add_assistant_message(
                conversation_id=conversation_id,
                content=response,
            )

            return response

        finally:
            db.close()