from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class CompilerSettings:
    """Configuration values for the compiler service and its components."""

    max_tokens: int = 160
    preferred_tokens: int = 100
    enable_token_aware_optimization: bool = True
    enable_validation: bool = True


def get_settings() -> CompilerSettings:
    """Return settings from the current environment."""
    return CompilerSettings(
        max_tokens=int(os.getenv("PROMPT_COMPILER_MAX_TOKENS", "160")),
        preferred_tokens=int(os.getenv("PROMPT_COMPILER_PREFERRED_TOKENS", "100")),
        enable_token_aware_optimization=os.getenv(
            "PROMPT_COMPILER_ENABLE_TOKEN_AWARE_OPTIMIZATION",
            "true",
        ).lower() == "true",
        enable_validation=os.getenv("PROMPT_COMPILER_ENABLE_VALIDATION", "true").lower() == "true",
    )
