from __future__ import annotations

from prompt_compiler.compiler.contracts import (
    Analyzer,
    IntentDetector,
    Optimizer,
    Scorer,
    TechniqueSelector,
    Validator,
)
from prompt_compiler.models.prompt_models import (
    OptimizationResult,
    Prompt,
    PromptAnalysis,
    PromptScore,
)


class PromptCompiler:
    """Coordinates prompt analysis, optimization, scoring, and validation."""

    def __init__(
        self,
        analyzer: Analyzer,
        intent_detector: IntentDetector,
        technique_selector: TechniqueSelector,
        optimizer: Optimizer,
        validator: Validator,
        scorer: Scorer,
    ) -> None:
        self._analyzer = analyzer
        self._intent_detector = intent_detector
        self._technique_selector = technique_selector
        self._optimizer = optimizer
        self._validator = validator
        self._scorer = scorer

    def compile(self, prompt: Prompt) -> OptimizationResult:
        """Run the prompt compilation pipeline and return the result."""
        analysis = self._analyzer.analyze(prompt)
        self._intent_detector.detect(prompt)
        self._technique_selector.select(prompt, analysis)

        optimized_prompt = self._optimizer.optimize(prompt, analysis)
        is_valid = self._validator.validate(optimized_prompt)
        score_before = self._scorer.score(prompt)
        score_after = self._scorer.score(optimized_prompt)

        return OptimizationResult(
            original_prompt=prompt,
            optimized_prompt=optimized_prompt,
            analysis=analysis,
            score_before=score_before,
            score_after=score_after,
            improvement=score_after.overall - score_before.overall,
            notes=["validation passed"] if is_valid else ["validation failed"],
        )


class PlaceholderAnalyzer(Analyzer):
    """Default analyzer implementation that returns a neutral analysis."""

    def analyze(self, prompt: Prompt) -> PromptAnalysis:
        return PromptAnalysis(prompt=prompt, score=PromptScore())


class PlaceholderIntentDetector(IntentDetector):
    """Default detector that returns an unknown intent label."""

    def detect(self, prompt: Prompt) -> str:
        return "unknown"


class PlaceholderTechniqueSelector(TechniqueSelector):
    """Default selector that chooses no techniques."""

    def select(self, prompt: Prompt, analysis: PromptAnalysis) -> list[str]:
        return []


class PlaceholderOptimizer(Optimizer):
    """Default optimizer that leaves the prompt unchanged."""

    def optimize(self, prompt: Prompt, analysis: PromptAnalysis) -> Prompt:
        return prompt


class PlaceholderValidator(Validator):
    """Default validator that accepts all prompts."""

    def validate(self, prompt: Prompt) -> bool:
        return True


class PlaceholderScorer(Scorer):
    """Default scorer that assigns a neutral score."""

    def score(self, prompt: Prompt) -> PromptScore:
        return PromptScore()
