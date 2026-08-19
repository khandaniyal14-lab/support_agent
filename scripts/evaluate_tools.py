import json

from app.evaluation.tools import ToolEvaluator


def main() -> None:

    evaluator = ToolEvaluator()

    results = evaluator.evaluate(
        "data/evaluation/tools.json"
    )

    print()
    print("=" * 70)
    print("TOOL EVALUATION")
    print("=" * 70)

    print()

    print(
        "Tool Selection Accuracy: "
        f"{results['tool_selection_accuracy']:.4f}"
    )

    print(
        "Tool Argument Accuracy : "
        f"{results['tool_argument_accuracy']:.4f}"
    )

    print(
        f"Total Cases            : "
        f"{results['total_cases']}"
    )

    print()
    print("DETAILS")
    print("-" * 70)

    for item in results["details"]:

        print()
        print(f"ID: {item['id']}")

        print(
            f"Expected Tool : "
            f"{item['expected_tool']}"
        )

        print(
            f"Predicted Tool: "
            f"{item['predicted_tool']}"
        )

        print(
            f"Expected Args : "
            f"{item['expected_arguments']}"
        )

        print(
            f"Predicted Args: "
            f"{item['predicted_arguments']}"
        )

        print(
            f"Tool Correct  : "
            f"{item['tool_correct']}"
        )

        print(
            f"Args Correct  : "
            f"{item['arguments_correct']}"
        )

    with open(
        "data/evaluation/tools_results.json",
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