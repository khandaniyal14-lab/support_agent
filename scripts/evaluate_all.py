from app.evaluation.run_all import (
    EvaluationRunner,
)


def main() -> None:

    runner = EvaluationRunner()

    results = runner.run()

    print()
    print("=" * 70)
    print("PHASE 6 — COMPLETE EVALUATION")
    print("=" * 70)

    print()

    # -------------------------
    # RAG
    # -------------------------

    rag = results["rag"]

    print("RAG")
    print("-" * 70)

    print(
        f"Recall@5 : "
        f"{rag['recall_at_k']:.4f}"
    )

    print(
        f"MRR      : "
        f"{rag['mrr']:.4f}"
    )

    print(
        f"NDCG@5   : "
        f"{rag['ndcg_at_k']:.4f}"
    )

    print()

    # -------------------------
    # Tools
    # -------------------------

    tools = results["tools"]

    print("TOOLS")
    print("-" * 70)

    print(
        f"Tool Selection Accuracy: "
        f"{tools['tool_selection_accuracy']:.4f}"
    )

    print(
        f"Tool Argument Accuracy : "
        f"{tools['tool_argument_accuracy']:.4f}"
    )

    print()

    # -------------------------
    # Agent
    # -------------------------

    agent = results["agent"]

    print("AGENT")
    print("-" * 70)

    print(
        f"Task Success Rate : "
        f"{agent['task_success_rate']:.4f}"
    )

    print(
        f"Resolution Accuracy: "
        f"{agent['resolution_accuracy']:.4f}"
    )

    print(
        f"Escalation Accuracy: "
        f"{agent['escalation_accuracy']:.4f}"
    )

    print()

    # -------------------------
    # Performance
    # -------------------------

    performance = results[
        "performance"
    ]

    latency = performance["latency"]
    tokens = performance["tokens"]

    print("PERFORMANCE")
    print("-" * 70)

    print(
        f"Average Latency: "
        f"{latency['average_seconds']:.4f}s"
    )

    print(
        f"P95 Latency    : "
        f"{latency['p95_seconds']:.4f}s"
    )

    print(
        f"Error Rate     : "
        f"{performance['error_rate']:.4f}"
    )

    print(
        f"Input Tokens   : "
        f"{tokens['input']}"
    )

    print(
        f"Output Tokens  : "
        f"{tokens['output']}"
    )

    print(
        f"Total Tokens   : "
        f"{tokens['total']}"
    )

    print(
        f"Estimated Cost : "
        f"${performance['estimated_cost']:.6f}"
    )

    print()

    print("=" * 70)
    print(
        "Baseline saved to "
        "data/evaluation/baseline.json"
    )
    print("=" * 70)


if __name__ == "__main__":
    main()