import json
from pathlib import Path

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
)

from app.agents.graph.schemas import TicketAnalysis
from app.agents.prompt import CLASSIFICATION_PROMPT
from app.ai.llm import LLMService


class ClassificationEvaluator:

    def __init__(
        self,
        llm_service: LLMService | None = None,
    ) -> None:

        self.llm = (
            llm_service
            or LLMService()
        )

    def classify(
        self,
        ticket: str,
    ) -> TicketAnalysis:

        response = self.llm.generate_structured(
            system_prompt=CLASSIFICATION_PROMPT,
            user_prompt=ticket,
            response_format={
                "type": "json_object",
            },
        )

        return TicketAnalysis.model_validate_json(
            response
        )

    def evaluate(
        self,
        dataset_path: str,
    ) -> dict:

        path = Path(dataset_path)

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:

            dataset = json.load(file)

        expected_categories = []
        predicted_categories = []

        expected_priorities = []
        predicted_priorities = []

        expected_intents = []
        predicted_intents = []

        errors = []

        for item in dataset:

            expected_categories.append(
                item["category"]
            )

            expected_priorities.append(
                item["priority"]
            )

            expected_intents.append(
                item["intent"]
            )

            try:

                prediction = self.classify(
                    item["ticket"]
                )

                predicted_categories.append(
                    prediction.category
                )

                predicted_priorities.append(
                    prediction.priority
                )

                predicted_intents.append(
                    prediction.intent
                )

            except Exception as exc: # noqa: BLE001

                predicted_categories.append(
                    "ERROR"
                )

                predicted_priorities.append(
                    "ERROR"
                )

                predicted_intents.append(
                    "ERROR"
                )

                errors.append(
                    {
                        "id": item["id"],
                        "error": str(exc),
                    }
                )

        return {
            "category": self._metrics(
                expected_categories,
                predicted_categories,
            ),
            "intent": self._metrics(
                expected_intents,
                predicted_intents,
            ),
            "priority": self._metrics(
                expected_priorities,
                predicted_priorities,
            ),
            "errors": errors,
        }

    @staticmethod
    def _metrics(
        expected: list[str],
        predicted: list[str],
    ) -> dict:

        return {
            "accuracy": accuracy_score(
                expected,
                predicted,
            ),
            "precision": precision_score(
                expected,
                predicted,
                average="weighted",
                zero_division=0,
            ),
            "recall": recall_score(
                expected,
                predicted,
                average="weighted",
                zero_division=0,
            ),
            "f1": f1_score(
                expected,
                predicted,
                average="weighted",
                zero_division=0,
            ),
        }