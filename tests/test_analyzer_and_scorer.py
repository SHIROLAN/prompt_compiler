from __future__ import annotations

from prompt_compiler.analyzer.heuristic_analyzer import HeuristicAnalyzer
from prompt_compiler.models.prompt_models import Prompt
from prompt_compiler.scorer.heuristic_scorer import HeuristicScorer


def test_analyzer_detects_intent_and_techniques() -> None:
    analyzer = HeuristicAnalyzer()
    prompt = Prompt(content="Summarize the report and provide examples.")

    analysis = analyzer.analyze(prompt)

    assert analysis.intent is not None
    assert analysis.intent.category.value == "summarization"
    assert any(tech.kind.value == "few_shot" for tech in analysis.detected_techniques)


def test_scorer_assigns_expected_scores() -> None:
    scorer = HeuristicScorer()
    prompt = Prompt(content="Summarize the report in a clear format.")

    score = scorer.score(prompt)

    assert score.clarity >= 0.7
    assert score.specificity >= 0.4
    assert score.completeness >= 0.6
    assert score.overall >= 0.6
