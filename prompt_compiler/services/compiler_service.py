from __future__ import annotations

from prompt_compiler.analyzer.heuristic_analyzer import HeuristicAnalyzer
from prompt_compiler.compiler.prompt_compiler import PromptCompiler
from prompt_compiler.config.settings import CompilerSettings, get_settings
from prompt_compiler.detector.heuristic_intent_detector import HeuristicIntentDetector
from prompt_compiler.models.prompt_models import OptimizationResult, Prompt
from prompt_compiler.optimizer.token_aware_optimizer import TokenAwareOptimizer
from prompt_compiler.scorer.heuristic_scorer import HeuristicScorer
from prompt_compiler.techniques.intent_based_selector import IntentBasedTechniqueSelector
from prompt_compiler.tokenizer.token_budget import TokenBudget
from prompt_compiler.validator.rule_based_validator import RuleBasedValidator


class CompilerService:
    """Application service that wires the compiler from configuration."""

    def __init__(self, settings: CompilerSettings | None = None) -> None:
        self._settings = settings or get_settings()
        self._compiler = self._build_compiler()

    def _build_compiler(self) -> PromptCompiler:
        budget = TokenBudget(
            max_tokens=self._settings.max_tokens,
            preferred_tokens=self._settings.preferred_tokens,
        )
        return PromptCompiler(
            analyzer=HeuristicAnalyzer(),
            intent_detector=HeuristicIntentDetector(),
            technique_selector=IntentBasedTechniqueSelector(),
            optimizer=TokenAwareOptimizer(budget),
            validator=RuleBasedValidator(),
            scorer=HeuristicScorer(),
        )

    def compile_prompt(self, prompt: str) -> OptimizationResult:
        """Compile a prompt string and return the optimization result."""
        return self._compiler.compile(Prompt(content=prompt))
