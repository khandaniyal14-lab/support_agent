from app.evaluation.agent import AgentEvaluator


def test_agent_evaluation():

    evaluator = AgentEvaluator()

    results = evaluator.evaluate(
        "data/evaluation/agents.json"
    )

    assert (
        0.0
        <= results["task_success_rate"]
        <= 1.0
    )

    assert (
        0.0
        <= results["resolution_accuracy"]
        <= 1.0
    )

    assert (
        0.0
        <= results["escalation_accuracy"]
        <= 1.0
    )

    assert results["total_cases"] > 0