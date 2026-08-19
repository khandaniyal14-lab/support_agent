import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.evaluation.agent import AgentEvaluator
from app.evaluation.performance import PerformanceEvaluator
from app.evaluation.rag import RAGEvaluator
from app.evaluation.tools import ToolEvaluator


class EvaluationRunner:

    def run(self) -> dict[str, Any]:

        results: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "classification": {},
            "rag": {},
            "tools": {},
            "agent": {},
            "performance": {},
        }

        # -------------------------
        # RAG
        # -------------------------

        rag_evaluator = RAGEvaluator()

        results["rag"] = rag_evaluator.evaluate(
            dataset_path="data/evaluation/rag.json",
            k=5,
        )

        # -------------------------
        # Tools
        # -------------------------

        tool_evaluator = ToolEvaluator()

        results["tools"] = tool_evaluator.evaluate(
            dataset_path="data/evaluation/tools.json",
        )

        # -------------------------
        # Agent
        # -------------------------

        agent_evaluator = AgentEvaluator()

        results["agent"] = agent_evaluator.evaluate(
            dataset_path="data/evaluation/agents.json",
        )

        # -------------------------
        # Performance
        # -------------------------

        performance_evaluator = (
            PerformanceEvaluator()
        )

        results["performance"] = (
            performance_evaluator.evaluate(
                dataset_path="data/evaluation/agents.json",
            )
        )

        # -------------------------
        # Save
        # -------------------------

        output_path = Path(
            "data/evaluation/baseline.json"
        )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with output_path.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                results,
                file,
                indent=2,
            )

        return results