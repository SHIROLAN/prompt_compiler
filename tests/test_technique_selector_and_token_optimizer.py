from __future__ import annotations

from prompt_compiler.analyzer.heuristic_analyzer import HeuristicAnalyzer
from prompt_compiler.models.prompt_models import Prompt
from prompt_compiler.optimizer.token_aware_optimizer import TokenAwareOptimizer
from prompt_compiler.techniques.intent_based_selector import IntentBasedTechniqueSelector
from prompt_compiler.tokenizer.token_budget import TokenBudget


def test_technique_selector_chooses_techniques_for_summary_prompt() -> None:
    selector = IntentBasedTechniqueSelector()
    analyzer = HeuristicAnalyzer()
    prompt = Prompt(content="Summarize the report and provide examples.")
    analysis = analyzer.analyze(prompt)

    selected = selector.select(prompt, analysis)

    assert "chain_of_thought" in selected
    assert "few_shot" in selected


def test_token_aware_optimizer_respects_budget_and_keeps_prompt_concise() -> None:
    optimizer = TokenAwareOptimizer(TokenBudget(max_tokens=80, preferred_tokens=40))
    analyzer = HeuristicAnalyzer()
    prompt = Prompt(content="Summarize the report in a clear format for executives.")
    analysis = analyzer.analyze(prompt)

    optimized = optimizer.optimize(prompt, analysis)

    assert "token budget" in optimized.content.lower()
    assert len(optimized.content.split()) <= 40
