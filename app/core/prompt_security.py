import re

INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"ignore\s+(all\s+)?prior\s+instructions",
    r"disregard\s+(all\s+)?previous\s+instructions",
    r"forget\s+(all\s+)?previous\s+instructions",
    r"system\s+prompt",
    r"reveal\s+(your\s+)?instructions",
    r"show\s+(me\s+)?your\s+prompt",
    r"developer\s+message",
    r"bypass\s+security",
    r"disable\s+safety",
]


def detect_prompt_injection(
    text: str,
) -> bool:

    normalized = text.lower()

    for pattern in INJECTION_PATTERNS:

        if re.search(
            pattern,
            normalized,
        ):
            return True

    return False