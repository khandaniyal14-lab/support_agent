import json

from app.evaluation.agent import AgentEvaluator


def main() -> None:

    evaluator = AgentEvaluator()

    results = evaluator.evaluate(
        "data/evaluation/agents.json"
    )

    print()
    print("=" * 70)
    print("AGENT EVALUATION")
    print("=" * 70)

    print()

    print(
        "Task Success Rate : "
        f"{results['task_success_rate']:.4f}"
    )

    print(
        "Resolution Accuracy: "
        f"{results['resolution_accuracy']:.4f}"
    )

    print(
        "Escalation Accuracy: "
        f"{results['escalation_accuracy']:.4f}"
    )

    print(
        "Total Cases        : "
        f"{results['total_cases']}"
    )

    print()
    print("DETAILS")
    print("-" * 70)

    for item in results["details"]:

        print()
        print(f"ID: {item['id']}")

        if "error" in item:
            print(
                f"ERROR: {item['error']}"
            )
            continue

        print(
            f"Task Success: "
            f"{item['task_success']}"
        )

        print(
            f"Resolution Correct: "
            f"{item['resolution_correct']}"
        )

        print(
            f"Escalation Correct: "
            f"{item['escalation_correct']}"
        )

        print(
            f"Response: "
            f"{item['response']}"
        )

    with open(
        "data/evaluation/agent_results.json",
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