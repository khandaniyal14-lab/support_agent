import time

import pytest

from app.core.retry import (
    RetryError,
    retry_with_backoff,
)
from app.core.timeout import (
    OperationTimeoutError,
    execute_with_timeout,
)


def test_retry_eventually_succeeds():

    attempts = 0

    def unstable_function():

        nonlocal attempts

        attempts += 1

        if attempts < 3:
            raise RuntimeError(
                "Temporary failure"
            )

        return "success"

    result = retry_with_backoff(
        unstable_function
    )

    assert result == "success"
    assert attempts == 3




def test_retry_fails_after_max_retries():

    attempts = 0

    def failing_function():

        nonlocal attempts

        attempts += 1

        raise RuntimeError(
            "Permanent failure"
        )

    with pytest.raises(
        RetryError
    ):
        retry_with_backoff(
            failing_function
        )

    assert attempts == 4







def test_operation_timeout():

    def slow_function():

        time.sleep(2)

        return "finished"

    with pytest.raises(
        OperationTimeoutError
    ):
        execute_with_timeout(
            slow_function,
            timeout=0.1,
        )

def test_operation_finishes_before_timeout():

    def fast_function():

        return "success"

    result = execute_with_timeout(
        fast_function,
        timeout=1,
    )

    assert result == "success"