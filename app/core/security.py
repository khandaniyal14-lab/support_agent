from dataclasses import dataclass


@dataclass(frozen=True)
class SecurityConfig:
    max_input_length: int = 10_000
    max_output_length: int = 10_000
    max_tool_calls: int = 10
    max_agent_iterations: int = 10


SECURITY_CONFIG = SecurityConfig()