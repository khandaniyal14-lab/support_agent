from dataclasses import dataclass


@dataclass(frozen=True)
class ReliabilityConfig:
    max_retries: int = 3
    retry_delay_seconds: float = 1.0
    request_timeout_seconds: float = 30.0


RELIABILITY_CONFIG = ReliabilityConfig()