from collections.abc import Callable
from typing import Any

from app.core.retry import (
    retry_with_backoff,
)
from app.core.timeout import (
    execute_with_timeout,
)


def execute_resilient(
    function: Callable[..., Any],
    *args: Any,
    timeout: float | None = None,
    **kwargs: Any,
) -> Any:

    def operation() -> Any:

        return execute_with_timeout(
            function,
            *args,
            timeout=timeout,
            **kwargs,
        )

    return retry_with_backoff(
        operation
    )