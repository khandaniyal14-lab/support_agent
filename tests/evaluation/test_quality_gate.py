import pytest

from app.evaluation.quality_gate import (
    EvaluationQualityError,
    check_classification_quality,
    check_rag_quality,
)


def test_classification_quality_passes():

    results = {
        "accuracy": 0.90,
        "f1": 0.88,
    }

    check_classification_quality(
        results
    )


def test_classification_quality_fails():

    results = {
        "accuracy": 0.70,
        "f1": 0.75,
    }

    with pytest.raises(
        EvaluationQualityError
    ):
        check_classification_quality(
            results
        )


def test_rag_quality_passes():

    results = {
        "recall_at_k": 1.0,
        "mrr": 0.82,
        "ndcg_at_k": 0.87,
    }

    check_rag_quality(
        results
    )


def test_rag_quality_fails():

    results = {
        "recall_at_k": 0.60,
        "mrr": 0.50,
        "ndcg_at_k": 0.55,
    }

    with pytest.raises(
        EvaluationQualityError
    ):
        check_rag_quality(
            results
        )