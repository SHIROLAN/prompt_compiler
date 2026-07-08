from __future__ import annotations

import pytest

from prompt_compiler.compiler.prompt_compiler import (
    PromptCompiler,
    PlaceholderAnalyzer,
    PlaceholderIntentDetector,
    PlaceholderOptimizer,
    PlaceholderScorer,
    PlaceholderTechniqueSelector,
    PlaceholderValidator,
)
from prompt_compiler.models.prompt_models import Prompt


def test_compiler_returns_optimization_result_for_valid_prompt() -> None:
    compiler = PromptCompiler(
        analyzer=PlaceholderAnalyzer(),
        intent_detector=PlaceholderIntentDetector(),
        technique_selector=PlaceholderTechniqueSelector(),
        optimizer=PlaceholderOptimizer(),
        validator=PlaceholderValidator(),
        scorer=PlaceholderScorer(),
    )

    prompt = Prompt(content="Summarize the benefits of exercise.")
    result = compiler.compile(prompt)

    assert result.original_prompt == prompt
    assert result.optimized_prompt == prompt
    assert result.score_before.overall == pytest.approx(0.5)
    assert result.score_after.overall == pytest.approx(0.5)
    assert result.notes == ["validation passed"]
