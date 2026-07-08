from __future__ import annotations

from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class IntentCategory(str, Enum):
    """High-level categories for prompt intent."""

    CLASSIFICATION = "classification"
    SUMMARIZATION = "summarization"
    GENERATION = "generation"
    EXTRACTION = "extraction"
    TRANSLATION = "translation"
    CODING = "coding"
    REASONING = "reasoning"


class TechniqueKind(str, Enum):
    """Supported prompt-engineering techniques."""

    FEW_SHOT = "few_shot"
    CHAIN_OF_THOUGHT = "chain_of_thought"
    ROLE_PROMPTING = "role_prompting"
    CONTEXTUAL_RETRIEVAL = "contextual_retrieval"
    SELF_CRITIQUE = "self_critique"
    TREE_OF_THOUGHT = "tree_of_thought"


class Prompt(BaseModel):
    """A prompt submitted for compilation."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    content: str = Field(..., min_length=1)
    context: dict[str, Any] = Field(default_factory=dict)
    version: int = Field(default=1, ge=1)

    model_config = ConfigDict(frozen=True, extra="forbid")


class Intent(BaseModel):
    """The inferred intent of a prompt."""

    category: IntentCategory
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    explanation: str = Field(default="")

    model_config = ConfigDict(frozen=True, extra="forbid")


class Technique(BaseModel):
    """A prompt engineering technique associated with a prompt."""

    kind: TechniqueKind
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    rationale: str = Field(default="")

    model_config = ConfigDict(frozen=True, extra="forbid")


class PromptScore(BaseModel):
    """A quality score for a prompt."""

    clarity: float = Field(default=0.5, ge=0.0, le=1.0)
    specificity: float = Field(default=0.5, ge=0.0, le=1.0)
    completeness: float = Field(default=0.5, ge=0.0, le=1.0)
    overall: float = Field(default=0.5, ge=0.0, le=1.0)

    model_config = ConfigDict(frozen=True, extra="forbid")


class PromptAnalysis(BaseModel):
    """The analysis output for a prompt."""

    prompt: Prompt
    intent: Intent | None = None
    detected_techniques: list[Technique] = Field(default_factory=list)
    score: PromptScore = Field(default_factory=PromptScore)
    summary: str = Field(default="")
    concerns: list[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True, extra="forbid")


class OptimizationResult(BaseModel):
    """The result of compiling and optimizing a prompt."""

    original_prompt: Prompt
    optimized_prompt: Prompt
    analysis: PromptAnalysis
    score_before: PromptScore
    score_after: PromptScore
    improvement: float = Field(default=0.0, ge=-1.0, le=1.0)
    notes: list[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True, extra="forbid")
