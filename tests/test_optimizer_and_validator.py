from __future__ import annotations

from prompt_compiler.analyzer.heuristic_analyzer import HeuristicAnalyzer
from prompt_compiler.models.prompt_models import Intent, IntentCategory, Prompt, PromptAnalysis, PromptScore
from prompt_compiler.optimizer.rule_based_optimizer import RuleBasedOptimizer
from prompt_compiler.validator.rule_based_validator import RuleBasedValidator


def test_optimizer_rewrites_prompt_for_clarity() -> None:
    optimizer = RuleBasedOptimizer()
    analyzer = HeuristicAnalyzer()
    prompt = Prompt(content="Summarize this.")
    analysis = analyzer.analyze(prompt)

    optimized = optimizer.optimize(prompt, analysis)

    assert optimized.content != prompt.content
    assert "Summarize" in optimized.content or "summarize" in optimized.content
    assert "Original request" in optimized.content


def test_validator_accepts_well_formed_prompt_and_rejects_short_one() -> None:
    validator = RuleBasedValidator()

    valid_prompt = Prompt(content="Summarize the report clearly and concisely for a busy executive.")
    invalid_prompt = Prompt(content="Short.")

    assert validator.validate(valid_prompt) is True
    assert validator.validate(invalid_prompt) is False
