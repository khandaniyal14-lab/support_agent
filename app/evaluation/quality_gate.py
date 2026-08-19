from typing import Any

from app.core.evaluation_config import (
    EVALUATION_THRESHOLDS,
)


class EvaluationQualityError(
    RuntimeError
):
    pass


def check_classification_quality(
    results: dict[str, Any],
) -> None:

    accuracy = float(
        results["accuracy"]
    )

    f1 = float(
        results["f1"]
    )

    if (
        accuracy
        < EVALUATION_THRESHOLDS.classification_accuracy
    ):
        raise EvaluationQualityError(
            "Classification accuracy below "
            f"threshold: {accuracy:.4f} < "
            f"{EVALUATION_THRESHOLDS.classification_accuracy:.4f}"
        )

    if (
        f1
        < EVALUATION_THRESHOLDS.classification_f1
    ):
        raise EvaluationQualityError(
            "Classification F1 below "
            f"threshold: {f1:.4f} < "
            f"{EVALUATION_THRESHOLDS.classification_f1:.4f}"
        )


def check_rag_quality(
    results: dict[str, Any],
) -> None:

    recall_at_k = float(
        results["recall_at_k"]
    )

    mrr = float(
        results["mrr"]
    )

    ndcg_at_k = float(
        results["ndcg_at_k"]
    )

    if (
        recall_at_k
        < EVALUATION_THRESHOLDS.rag_recall_at_k
    ):
        raise EvaluationQualityError(
            "RAG Recall@K below threshold: "
            f"{recall_at_k:.4f} < "
            f"{EVALUATION_THRESHOLDS.rag_recall_at_k:.4f}"
        )

    if (
        mrr
        < EVALUATION_THRESHOLDS.rag_mrr
    ):
        raise EvaluationQualityError(
            "RAG MRR below threshold: "
            f"{mrr:.4f} < "
            f"{EVALUATION_THRESHOLDS.rag_mrr:.4f}"
        )

    if (
        ndcg_at_k
        < EVALUATION_THRESHOLDS.rag_ndcg_at_k
    ):
        raise EvaluationQualityError(
            "RAG NDCG@K below threshold: "
            f"{ndcg_at_k:.4f} < "
            f"{EVALUATION_THRESHOLDS.rag_ndcg_at_k:.4f}"
        )