from typing import Any

from mistralai.client import Mistral

from app.core.config import settings
from app.core.resilient import (
    execute_resilient,
)


class LLMService:
    def __init__(self) -> None:
        self.client = Mistral(
            api_key=settings.mistral_api_key
        )

        self.model = settings.mistral_model

    def generate_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        response_format: dict,
    ) -> str:

        def request():

            response = self.client.chat.complete(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                temperature=settings.llm_temperature,
                max_tokens=settings.llm_max_tokens,
                response_format=response_format,
            )

            content = (
                response
                .choices[0]
                .message
                .content
            )

            if not content:
                raise ValueError(
                    "LLM returned an empty response."
                )

            return content

        return execute_resilient(
            request
        )

    def generate(
        self,
        messages: list[Any],
        tools: list[Any] | None = None,
    ):
        request: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": settings.llm_temperature,
            "max_tokens": settings.llm_max_tokens,
        }

        if tools:
            request["tools"] = [
                tool_to_mistral_schema(tool)
                for tool in tools
            ]

        response = self.client.chat.complete(
            **request
        )

        return response.choices[0].message


def tool_to_mistral_schema(tool: Any) -> dict:
    """
    Convert a LangChain tool into the tool schema
    expected by Mistral.
    """

    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.args_schema.model_json_schema(),
        },
    }

    def generate_validated(
        self,
        system_prompt: str,
        user_prompt: str,
        response_format: dict,
    ) -> str:

        content = self.generate_structured(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        if not content.strip():
            raise ValueError(
                "LLM returned empty output."
            )

        return content