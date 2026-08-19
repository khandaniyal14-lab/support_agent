import json
import time
from pathlib import Path
from typing import Any

from app.agents.support_agent import SupportAgent


class PerformanceEvaluator:

    def __init__(
        self,
        agent: SupportAgent | None = None,
    ) -> None:

        self.agent = agent or SupportAgent()

    def evaluate(
        self,
        dataset_path: str,
    ) -> dict[str, Any]:

        path = Path(dataset_path)

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            dataset = json.load(file)

        latencies = []
        errors = []

        total_input_tokens = 0
        total_output_tokens = 0

        details = []

        for index, item in enumerate(dataset):

            conversation_id = (
                f"performance-{index}"
            )

            start_time = time.perf_counter()

            try:

                response = self.agent.run(
                    request=item["request"],
                    conversation_id=conversation_id,
                )

                elapsed = (
                    time.perf_counter()
                    - start_time
                )

                latencies.append(elapsed)

                input_tokens = self._estimate_tokens(
                    item["request"]
                )

                output_tokens = self._estimate_tokens(
                    response
                )

                total_input_tokens += (
                    input_tokens
                )

                total_output_tokens += (
                    output_tokens
                )

                details.append(
                    {
                        "id": item["id"],
                        "latency_seconds": elapsed,
                        "input_tokens": input_tokens,
                        "output_tokens": output_tokens,
                        "error": None,
                    }
                )

            except Exception as exc: # noqa: BLE001

                elapsed = (
                    time.perf_counter()
                    - start_time
                )

                latencies.append(elapsed)

                errors.append(
                    {
                        "id": item["id"],
                        "error": str(exc),
                    }
                )

                details.append(
                    {
                        "id": item["id"],
                        "latency_seconds": elapsed,
                        "input_tokens": 0,
                        "output_tokens": 0,
                        "error": str(exc),
                    }
                )

        total_requests = len(dataset)

        successful_requests = (
            total_requests
            - len(errors)
        )

        return {
            "total_requests": total_requests,
            "successful_requests": successful_requests,
            "error_count": len(errors),
            "error_rate": (
                len(errors) / total_requests
                if total_requests
                else 0.0
            ),
            "latency": self._latency_metrics(
                latencies
            ),
            "tokens": {
                "input": total_input_tokens,
                "output": total_output_tokens,
                "total": (
                    total_input_tokens
                    + total_output_tokens
                ),
            },
            "estimated_cost": self._estimate_cost(
                total_input_tokens,
                total_output_tokens,
            ),
            "errors": errors,
            "details": details,
        }

    @staticmethod
    def _latency_metrics(
        latencies: list[float],
    ) -> dict[str, float]:

        if not latencies:
            return {
                "average_seconds": 0.0,
                "min_seconds": 0.0,
                "max_seconds": 0.0,
                "p95_seconds": 0.0,
            }

        ordered = sorted(latencies)

        p95_index = min(
            int(len(ordered) * 0.95),
            len(ordered) - 1,
        )

        return {
            "average_seconds": (
                sum(latencies)
                / len(latencies)
            ),
            "min_seconds": min(latencies),
            "max_seconds": max(latencies),
            "p95_seconds": ordered[p95_index],
        }

    @staticmethod
    def _estimate_tokens(
        text: str,
    ) -> int:

        if not text:
            return 0

        return max(
            1,
            len(text.split()) * 4 // 3,
        )

    @staticmethod
    def _estimate_cost(
        input_tokens: int,
        output_tokens: int,
    ) -> float:

        # Placeholder pricing for evaluation.
        # Replace with the exact model pricing
        # used by your deployment.

        input_price_per_million = 0.50
        output_price_per_million = 1.50

        input_cost = (
            input_tokens
            / 1_000_000
            * input_price_per_million
        )

        output_cost = (
            output_tokens
            / 1_000_000
            * output_price_per_million
        )

        return input_cost + output_cost