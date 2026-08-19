from app.evaluation.classification import (
    ClassificationEvaluator,
)


def test_classification_evaluation():

    evaluator = ClassificationEvaluator()

    results = evaluator.evaluate(
        "data/evaluation/classification.json"
    )

    assert "category" in results
    assert "intent" in results
    assert "priority" in results

    assert (
        0.0
        <= results["category"]["accuracy"]
        <= 1.0
    )

    assert (
        0.0
        <= results["intent"]["accuracy"]
        <= 1.0
    )

    assert (
        0.0
        <= results["priority"]["accuracy"]
        <= 1.0
    )