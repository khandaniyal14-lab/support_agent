import json
import sys
from pathlib import Path

from app.agents.graph.schemas import TicketAnalysis
from app.agents.prompt import CLASSIFICATION_PROMPT
from app.ai.llm import LLMService
from app.evaluation.quality_gate import (
    check_classification_quality,
)


def main() -> None:

    dataset_path = Path(
        "data/evaluation/classification.json"
    )

    with dataset_path.open(
        "r",
        encoding="utf-8",
    ) as file:

        dataset = json.load(file)

    llm = LLMService()

    total = len(dataset)

    correct_category = 0
    correct_intent = 0

    for item in dataset:

        result = llm.generate_structured(
            system_prompt=CLASSIFICATION_PROMPT,
            user_prompt=item["ticket"],
            response_format={
                "type": "json_object"
            },
        )

        prediction = TicketAnalysis.model_validate_json(
            result
        )

        if (
            prediction.category
            == item["category"]
        ):
            correct_category += 1

        if (
            prediction.intent
            == item["intent"]
        ):
            correct_intent += 1

    accuracy = (
        correct_category / total
        if total
        else 0.0
    )

    f1 = (
        correct_intent / total
        if total
        else 0.0
    )

    results = {
        "accuracy": accuracy,
        "f1": f1,
    }

    print(
        json.dumps(
            results,
            indent=2,
        )
    )

    check_classification_quality(
        results
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(
            f"Evaluation failed: {exc}"
        )
        sys.exit(1)