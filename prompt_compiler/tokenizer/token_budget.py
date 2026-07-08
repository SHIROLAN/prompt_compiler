from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TokenBudget:
    """A simple token budget for prompt optimization."""

    max_tokens: int = 180
    preferred_tokens: int = 120
