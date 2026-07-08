from __future__ import annotations

from fastapi import FastAPI

from prompt_compiler.analyzer.heuristic_analyzer import HeuristicAnalyzer
from prompt_compiler.compiler.prompt_compiler import PromptCompiler
from prompt_compiler.detector.heuristic_intent_detector import HeuristicIntentDetector
from prompt_compiler.models.prompt_models import Prompt
from prompt_compiler.optimizer.token_aware_optimizer import TokenAwareOptimizer
from prompt_compiler.scorer.heuristic_scorer import HeuristicScorer
from prompt_compiler.techniques.intent_based_selector import IntentBasedTechniqueSelector
from prompt_compiler.tokenizer.token_budget import TokenBudget
from prompt_compiler.validator.rule_based_validator import RuleBasedValidator
from prompt_compiler.api.schemas import CompileRequest, CompileResponse

app = FastAPI(title="Prompt Compiler API", version="0.1.0")

compiler = PromptCompiler(
    analyzer=HeuristicAnalyzer(),
    intent_detector=HeuristicIntentDetector(),
    technique_selector=IntentBasedTechniqueSelector(),
    optimizer=TokenAwareOptimizer(TokenBudget(max_tokens=160, preferred_tokens=100)),
    validator=RuleBasedValidator(),
    scorer=HeuristicScorer(),
)


@app.get("/health")
def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/compile", response_model=CompileResponse)
def compile_prompt(request: CompileRequest) -> CompileResponse:
    """Compile a prompt and return the optimized result."""
    prompt = Prompt(content=request.content, context=request.context)
    result = compiler.compile(prompt)

    return CompileResponse(
        original_prompt=result.original_prompt.content,
        optimized_prompt=result.optimized_prompt.content,
        intent=result.analysis.intent.category.value if result.analysis.intent else None,
        techniques=[tech.kind.value for tech in result.analysis.detected_techniques],
        score_before=result.score_before.overall,
        score_after=result.score_after.overall,
        notes=result.notes,
    )
