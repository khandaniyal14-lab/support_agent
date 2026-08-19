import json
from pathlib import Path
from typing import Any

from app.ai.llm import LLMService


class ToolEvaluator:

    def __init__(
        self,
        llm_service: LLMService | None = None,
    ) -> None:

        self.llm = (
            llm_service
            or LLMService()
        )

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

        tool_correct = 0
        arguments_correct = 0

        total = len(dataset)

        details = []

        for item in dataset:

            prediction = self._select_tool(
                item["request"]
            )

            predicted_tool = prediction[
                "tool"
            ]

            predicted_arguments = prediction[
                "arguments"
            ]

            expected_tool = item[
                "expected_tool"
            ]

            expected_arguments = item[
                "expected_arguments"
            ]

            is_tool_correct = (
                predicted_tool
                == expected_tool
            )

            is_arguments_correct = (
                predicted_arguments
                == expected_arguments
            )

            if is_tool_correct:
                tool_correct += 1

            if is_arguments_correct:
                arguments_correct += 1

            details.append(
                {
                    "id": item["id"],
                    "request": item["request"],
                    "expected_tool": expected_tool,
                    "predicted_tool": predicted_tool,
                    "expected_arguments": expected_arguments,
                    "predicted_arguments": predicted_arguments,
                    "tool_correct": is_tool_correct,
                    "arguments_correct": is_arguments_correct,
                }
            )

        return {
            "tool_selection_accuracy": (
                tool_correct / total
                if total
                else 0.0
            ),
            "tool_argument_accuracy": (
                arguments_correct / total
                if total
                else 0.0
            ),
            "total_cases": total,
            "details": details,
        }

    def _select_tool(
        self,
        request: str,
    ) -> dict[str, Any]:

        system_prompt = """
You are a customer support tool-selection evaluator.

Select exactly one tool from this list:

get_customer
get_order
get_payment_status
get_previous_tickets
check_refund_status
search_knowledge_base

Return ONLY valid JSON.

Format:

{
  "tool": "tool_name",
  "arguments": {}
}

Rules:

- get_customer requires no arguments.
- get_previous_tickets requires no arguments.
- get_order requires order_id.
- get_payment_status requires order_id.
- check_refund_status requires order_id.
- search_knowledge_base requires query.
"""

        response = self.llm.generate_structured(
            system_prompt=system_prompt,
            user_prompt=request,
            response_format={
                "type": "json_object",
            },
        )

        return json.loads(response)