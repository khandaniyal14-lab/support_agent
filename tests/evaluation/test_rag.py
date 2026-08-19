from app.evaluation.rag import RAGEvaluator


def test_rag_evaluation():

    evaluator = RAGEvaluator()

    results = evaluator.evaluate(
        dataset_path="data/evaluation/rag.json",
        k=5,
    )

    assert "recall_at_k" in results
    assert "mrr" in results
    assert "ndcg_at_k" in results

    assert (
        0.0
        <= results["recall_at_k"]
        <= 1.0
    )

    assert (
        0.0
        <= results["mrr"]
        <= 1.0
    )

    assert (
        0.0
        <= results["ndcg_at_k"]
        <= 1.0
    )