import json
from pathlib import Path
from typing import Any

from app.agents.support_agent import SupportAgent


class AgentEvaluator:

    def __init__(
        self,
        agent: SupportAgent | None = None,
    ) -> None:

        self.agent = agent or SupportAgent()

    def evaluate(
        self,
        dataset_path: str,
    ) -> dict[str, Any]:

        path = Path(dataset_path)

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            dataset = json.load(file)

        total = len(dataset)

        successful_tasks = 0
        correct_resolutions = 0
        correct_escalations = 0

        details = []

        for item in dataset:

            conversation_id = (
                f"evaluation-{item['id']}"
            )

            try:

                response = self.agent.run(
                    request=item["request"],
                    conversation_id=conversation_id,
                )

                response_text = response.lower()

                expected_outcome = (
                    item["expected_outcome"]
                )

                expected_resolution = (
                    item["expected_resolution"]
                )

                expected_escalation = (
                    item["expected_escalation"]
                )

                actual_escalation = (
                    self._detect_escalation(
                        response_text
                    )
                )

                actual_resolution = (
                    self._detect_resolution(
                        response_text
                    )
                )

                task_success = (
                    actual_escalation
                    == expected_escalation
                )

                resolution_correct = (
                    expected_resolution
                    in response_text
                )

                escalation_correct = (
                    actual_escalation
                    == expected_escalation
                )

                if task_success:
                    successful_tasks += 1

                if resolution_correct:
                    correct_resolutions += 1

                if escalation_correct:
                    correct_escalations += 1

                details.append(
                    {
                        "id": item["id"],
                        "request": item["request"],
                        "expected_outcome": expected_outcome,
                        "expected_resolution": expected_resolution,
                        "expected_escalation": expected_escalation,
                        "actual_escalation": actual_escalation,
                        "actual_resolution": actual_resolution,
                        "task_success": task_success,
                        "resolution_correct": resolution_correct,
                        "escalation_correct": escalation_correct,
                        "response": response,
                    }
                )

            except Exception as exc:  # noqa: BLE001

                details.append(
                    {
                        "id": item["id"],
                        "request": item["request"],
                        "error": str(exc),
                        "task_success": False,
                        "resolution_correct": False,
                        "escalation_correct": False,
                    }
                )

        return {
            "task_success_rate": (
                successful_tasks / total
                if total
                else 0.0
            ),
            "resolution_accuracy": (
                correct_resolutions / total
                if total
                else 0.0
            ),
            "escalation_accuracy": (
                correct_escalations / total
                if total
                else 0.0
            ),
            "total_cases": total,
            "details": details,
        }

    @staticmethod
    def _detect_escalation(
        response: str,
    ) -> bool:

        escalation_terms = [
            "escalat",
            "human agent",
            "support agent",
            "specialist",
            "human review",
        ]

        return any(
            term in response
            for term in escalation_terms
        )

    @staticmethod
    def _detect_resolution(
        response: str,
    ) -> str:

        resolution_keywords = {
            "refund": [
                "refund",
                "reimbursement",
            ],
            "login_assistance": [
                "password",
                "login",
                "log in",
                "sign in",
            ],
            "order_cancellation_policy": [
                "cancel",
                "cancellation",
            ],
            "damaged_order": [
                "damaged",
                "defective",
                "replacement",
            ],
            "duplicate_charge": [
                "duplicate",
                "charged twice",
            ],
            "account_security": [
                "account security",
                "security",
                "account takeover",
            ],
            "refund_exception": [
                "refund",
                "exception",
                "policy",
            ],
            "payment_order_mismatch": [
                "payment",
                "order",
                "charge",
            ],
        }

        for resolution, keywords in (
            resolution_keywords.items()
        ):

            if any(
                keyword in response
                for keyword in keywords
            ):
                return resolution

        return "unknown"