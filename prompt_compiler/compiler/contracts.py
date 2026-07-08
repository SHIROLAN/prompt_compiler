from __future__ import annotations

from abc import ABC, abstractmethod

from prompt_compiler.models.prompt_models import Prompt, PromptAnalysis, PromptScore


class Analyzer(ABC):
    """Contract for analyzing a prompt prior to optimization."""

    @abstractmethod
    def analyze(self, prompt: Prompt) -> PromptAnalysis:
        """Return a structured analysis for the prompt."""


class IntentDetector(ABC):
    """Contract for detecting the intent of a prompt."""

    @abstractmethod
    def detect(self, prompt: Prompt) -> str:
        """Return a detected intent label or identifier."""


class TechniqueSelector(ABC):
    """Contract for selecting prompt-engineering techniques."""

    @abstractmethod
    def select(self, prompt: Prompt, analysis: PromptAnalysis) -> list[str]:
        """Return the techniques that should be applied."""


class Optimizer(ABC):
    """Contract for transforming a prompt into an optimized version."""

    @abstractmethod
    def optimize(self, prompt: Prompt, analysis: PromptAnalysis) -> Prompt:
        """Return an optimized prompt for the given analysis."""


class Validator(ABC):
    """Contract for validating prompts and optimization results."""

    @abstractmethod
    def validate(self, prompt: Prompt) -> bool:
        """Return True when the prompt passes validation rules."""


class Scorer(ABC):
    """Contract for scoring prompt quality."""

    @abstractmethod
    def score(self, prompt: Prompt) -> PromptScore:
        """Return a prompt quality score."""
