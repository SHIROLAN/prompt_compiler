from __future__ import annotations

import typer

from prompt_compiler.analyzer.heuristic_analyzer import HeuristicAnalyzer
from prompt_compiler.compiler.prompt_compiler import PromptCompiler
from prompt_compiler.detector.heuristic_intent_detector import HeuristicIntentDetector
from prompt_compiler.models.prompt_models import Prompt
from prompt_compiler.optimizer.token_aware_optimizer import TokenAwareOptimizer
from prompt_compiler.scorer.heuristic_scorer import HeuristicScorer
from prompt_compiler.techniques.intent_based_selector import IntentBasedTechniqueSelector
from prompt_compiler.tokenizer.token_budget import TokenBudget
from prompt_compiler.validator.rule_based_validator import RuleBasedValidator

app = typer.Typer(help="Compile and optimize prompts from the command line.")


@app.command()
def main(prompt: str = typer.Argument(..., help="The prompt to compile")) -> None:
    """Compile a prompt and print the optimized result."""
    compiler = PromptCompiler(
        analyzer=HeuristicAnalyzer(),
        intent_detector=HeuristicIntentDetector(),
        technique_selector=IntentBasedTechniqueSelector(),
        optimizer=TokenAwareOptimizer(TokenBudget(max_tokens=160, preferred_tokens=100)),
        validator=RuleBasedValidator(),
        scorer=HeuristicScorer(),
    )

    result = compiler.compile(Prompt(content=prompt))
    typer.echo(f"Original: {result.original_prompt.content}")
    typer.echo(f"Optimized: {result.optimized_prompt.content}")
    typer.echo(f"Intent: {result.analysis.intent.category.value if result.analysis.intent else 'none'}")
    typer.echo(f"Techniques: {', '.join(tech.kind.value for tech in result.analysis.detected_techniques) or 'none'}")
    typer.echo(f"Score: {result.score_after.overall:.2f}")


if __name__ == "__main__":
    app()
