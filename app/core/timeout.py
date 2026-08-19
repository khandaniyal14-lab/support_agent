from collections.abc import Callable
from concurrent.futures import (
    ThreadPoolExecutor,
    TimeoutError,
)
from typing import Any

from app.core.reliability import (
    RELIABILITY_CONFIG,
)


class OperationTimeoutError(
    TimeoutError
):
    pass


def execute_with_timeout(
    function: Callable[..., Any],
    *args: Any,
    timeout: float | None = None,
    **kwargs: Any,
) -> Any:

    timeout_seconds = (
        timeout
        or RELIABILITY_CONFIG.request_timeout_seconds
    )

    with ThreadPoolExecutor(
        max_workers=1
    ) as executor:

        future = executor.submit(
            function,
            *args,
            **kwargs,
        )

        try:

            return future.result(
                timeout=timeout_seconds
            )

        except TimeoutError as exc:

            future.cancel()

            raise OperationTimeoutError(
                "Operation exceeded the "
                f"{timeout_seconds} second timeout."
            ) from exc