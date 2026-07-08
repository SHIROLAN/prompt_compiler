from __future__ import annotations

from pydantic import BaseModel, Field


class CompileRequest(BaseModel):
    """Request payload for the compile endpoint."""

    content: str = Field(..., min_length=1, description="The prompt to compile")
    context: dict[str, str] = Field(default_factory=dict, description="Optional context metadata")


class CompileResponse(BaseModel):
    """Response payload for the compile endpoint."""

    original_prompt: str
    optimized_prompt: str
    intent: str | None
    techniques: list[str]
    score_before: float
    score_after: float
    notes: list[str]
