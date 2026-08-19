import json
import sys

from app.evaluation.quality_gate import (
    check_rag_quality,
)
from app.evaluation.rag import RAGEvaluator


def main() -> None:

    evaluator = RAGEvaluator()

    results = evaluator.evaluate(
        dataset_path="data/evaluation/rag.json",
        k=5,
    )

    print(
        json.dumps(
            results,
            indent=2,
        )
    )

    check_rag_quality(
        results
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(
            f"RAG evaluation failed: {exc}"
        )
        sys.exit(1)