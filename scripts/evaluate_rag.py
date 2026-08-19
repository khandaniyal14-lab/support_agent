import json

from app.evaluation.rag import RAGEvaluator


def main() -> None:

    evaluator = RAGEvaluator()

    results = evaluator.evaluate(
        dataset_path=(
            "data/evaluation/rag.json"
        ),
        k=5,
    )

    print()
    print("=" * 70)
    print("RAG EVALUATION")
    print("=" * 70)

    print()
    print(
        f"Recall@5 : "
        f"{results['recall_at_k']:.4f}"
    )

    print(
        f"MRR      : "
        f"{results['mrr']:.4f}"
    )

    print(
        f"NDCG@5   : "
        f"{results['ndcg_at_k']:.4f}"
    )

    print()
    print("QUERY DETAILS")
    print("-" * 70)

    for item in results["details"]:

        print()
        print(f"ID: {item['id']}")
        print(
            f"Question: "
            f"{item['question']}"
        )
        print(
            f"Expected: "
            f"{item['expected_source']}"
        )
        print(
            f"Retrieved: "
            f"{item['retrieved_sources']}"
        )

        print(
            f"Recall@5: "
            f"{item['recall_at_k']:.4f}"
        )

        print(
            f"RR: "
            f"{item['reciprocal_rank']:.4f}"
        )

        print(
            f"NDCG@5: "
            f"{item['ndcg_at_k']:.4f}"
        )

    with open(
        "data/evaluation/rag_results.json",
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