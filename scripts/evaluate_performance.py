import json

from app.evaluation.performance import (
    PerformanceEvaluator,
)


def main() -> None:

    evaluator = PerformanceEvaluator()

    results = evaluator.evaluate(
        "data/evaluation/agents.json"
    )

    print()
    print("=" * 70)
    print("SYSTEM PERFORMANCE EVALUATION")
    print("=" * 70)

    print()

    print(
        f"Total Requests : "
        f"{results['total_requests']}"
    )

    print(
        f"Successful     : "
        f"{results['successful_requests']}"
    )

    print(
        f"Errors         : "
        f"{results['error_count']}"
    )

    print(
        f"Error Rate     : "
        f"{results['error_rate']:.4f}"
    )

    print()
    print("LATENCY")
    print("-" * 70)

    latency = results["latency"]

    print(
        f"Average: "
        f"{latency['average_seconds']:.4f}s"
    )

    print(
        f"Minimum: "
        f"{latency['min_seconds']:.4f}s"
    )

    print(
        f"Maximum: "
        f"{latency['max_seconds']:.4f}s"
    )

    print(
        f"P95    : "
        f"{latency['p95_seconds']:.4f}s"
    )

    print()
    print("TOKENS")
    print("-" * 70)

    tokens = results["tokens"]

    print(
        f"Input : "
        f"{tokens['input']}"
    )

    print(
        f"Output: "
        f"{tokens['output']}"
    )

    print(
        f"Total : "
        f"{tokens['total']}"
    )

    print()
    print("ESTIMATED COST")
    print("-" * 70)

    print(
        f"${results['estimated_cost']:.6f}"
    )

    with open(
        "data/evaluation/performance_results.json",
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