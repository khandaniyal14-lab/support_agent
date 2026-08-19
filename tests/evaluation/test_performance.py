from app.evaluation.performance import (
    PerformanceEvaluator,
)


def test_performance_evaluation():

    evaluator = PerformanceEvaluator()

    results = evaluator.evaluate(
        "data/evaluation/agents.json"
    )

    assert results["total_requests"] > 0

    assert (
        0.0
        <= results["error_rate"]
        <= 1.0
    )

    assert (
        results["latency"]["average_seconds"]
        >= 0.0
    )

    assert (
        results["latency"]["p95_seconds"]
        >= 0.0
    )

    assert results["tokens"]["total"] >= 0

    assert (
        results["estimated_cost"]
        >= 0.0
    )