from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationThresholds:
    classification_accuracy: float = 0.80
    classification_f1: float = 0.80

    rag_recall_at_k: float = 0.80
    rag_mrr: float = 0.70
    rag_ndcg_at_k: float = 0.70


EVALUATION_THRESHOLDS = EvaluationThresholds()