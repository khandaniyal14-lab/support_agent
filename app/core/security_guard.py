from app.core.prompt_security import (
    detect_prompt_injection,
)
from app.core.validation import (
    validate_user_input,
)


class SecurityViolation(
    ValueError
):
    pass


def security_check(
    user_input: str,
) -> str:

    validated = validate_user_input(
        user_input
    )

    if detect_prompt_injection(
        validated
    ):
        raise SecurityViolation(
            "Potential prompt injection detected."
        )

    return validated