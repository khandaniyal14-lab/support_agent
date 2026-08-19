import json

from app.evaluation.classification import (
    ClassificationEvaluator,
)


def main() -> None:

    evaluator = ClassificationEvaluator()

    results = evaluator.evaluate(
        "data/evaluation/classification.json"
    )

    print()
    print("=" * 70)
    print("CLASSIFICATION EVALUATION")
    print("=" * 70)

    for name in [
        "category",
        "intent",
        "priority",
    ]:

        metrics = results[name]

        print()
        print(name.upper())
        print("-" * 70)

        print(
            f"Accuracy : "
            f"{metrics['accuracy']:.4f}"
        )

        print(
            f"Precision: "
            f"{metrics['precision']:.4f}"
        )

        print(
            f"Recall   : "
            f"{metrics['recall']:.4f}"
        )

        print(
            f"F1       : "
            f"{metrics['f1']:.4f}"
        )

    if results["errors"]:

        print()
        print("ERRORS")
        print("-" * 70)

        for error in results["errors"]:
            print(error)

    with open(
        "data/evaluation/classification_results.json",
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            results,
            file,
            indent=2,
        )


if __name__ == "__main__":
    main()