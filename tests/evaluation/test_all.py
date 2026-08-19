from app.evaluation.run_all import (
    EvaluationRunner,
)


def test_complete_evaluation():

    runner = EvaluationRunner()

    results = runner.run()

    assert "rag" in results
    assert "tools" in results
    assert "agent" in results
    assert "performance" in results

    # RAG

    assert (
        0.0
        <= results["rag"]["recall_at_k"]
        <= 1.0
    )

    assert (
        0.0
        <= results["rag"]["mrr"]
        <= 1.0
    )

    assert (
        0.0
        <= results["rag"]["ndcg_at_k"]
        <= 1.0
    )

    # Tools

    assert (
        0.0
        <= results["tools"][
            "tool_selection_accuracy"
        ]
        <= 1.0
    )

    assert (
        0.0
        <= results["tools"][
            "tool_argument_accuracy"
        ]
        <= 1.0
    )

    # Agent

    assert (
        0.0
        <= results["agent"][
            "task_success_rate"
        ]
        <= 1.0
    )

    assert (
        0.0
        <= results["agent"][
            "resolution_accuracy"
        ]
        <= 1.0
    )

    assert (
        0.0
        <= results["agent"][
            "escalation_accuracy"
        ]
        <= 1.0
    )

    # Performance

    assert (
        results["performance"][
            "error_rate"
        ]
        >= 0.0
    )

    assert (
        results["performance"]["latency"][
            "average_seconds"
        ]
        >= 0.0
    )