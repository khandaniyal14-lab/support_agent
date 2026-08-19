import time
from collections.abc import Callable
from typing import Any

from app.core.reliability import (
    RELIABILITY_CONFIG,
)


class RetryError(Exception):
    pass


def calculate_backoff(
    attempt: int,
) -> float:

    return (
        RELIABILITY_CONFIG.retry_delay_seconds
        * (2 ** attempt)
    )


def retry_with_backoff(
    function: Callable[..., Any],
    *args: Any,
    **kwargs: Any,
) -> Any:

    last_exception: Exception | None = None

    for attempt in range(
        RELIABILITY_CONFIG.max_retries + 1
    ):

        try:
            return function(
                *args,
                **kwargs,
            )

        except Exception as exc: # noqa: BLE001

            last_exception = exc

            if (
                attempt
                >= RELIABILITY_CONFIG.max_retries
            ):
                break

            delay = calculate_backoff(
                attempt
            )

            time.sleep(delay)

    raise RetryError(
        "Operation failed after "
        f"{RELIABILITY_CONFIG.max_retries} "
        "retries."
    ) from last_exception