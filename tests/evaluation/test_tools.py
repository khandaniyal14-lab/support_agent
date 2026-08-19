from app.evaluation.tools import ToolEvaluator


def test_tool_evaluation():

    evaluator = ToolEvaluator()

    results = evaluator.evaluate(
        "data/evaluation/tools.json"
    )

    assert (
        0.0
        <= results["tool_selection_accuracy"]
        <= 1.0
    )

    assert (
        0.0
        <= results["tool_argument_accuracy"]
        <= 1.0
    )

    assert results["total_cases"] > 0