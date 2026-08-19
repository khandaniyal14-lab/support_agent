from app.core.security import SECURITY_CONFIG


class SecurityValidationError(
    ValueError
):
    pass


def validate_user_input(
    text: str,
) -> str:

    if not isinstance(text, str):
        raise SecurityValidationError(
            "Input must be a string."
        )

    text = text.strip()

    if not text:
        raise SecurityValidationError(
            "Input cannot be empty."
        )

    if len(text) > (
        SECURITY_CONFIG.max_input_length
    ):
        raise SecurityValidationError(
            "Input exceeds maximum allowed length."
        )

    return text


def validate_output(
    text: str,
) -> str:

    if not isinstance(text, str):
        raise SecurityValidationError(
            "Output must be a string."
        )

    if len(text) > (
        SECURITY_CONFIG.max_output_length
    ):
        raise SecurityValidationError(
            "Output exceeds maximum allowed length."
        )

    return text