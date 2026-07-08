from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

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


@app.get("/", response_class=HTMLResponse)
def root() -> HTMLResponse:
    """Serve a simple browser-based UI for the prompt compiler."""
    return HTMLResponse(
        content="""
        <!doctype html>
        <html lang=\"en\">
        <head>
            <meta charset=\"utf-8\">
            <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
            <title>Prompt Compiler</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 900px; margin: 2rem auto; padding: 1rem; }
                textarea { width: 100%; min-height: 140px; margin-top: 0.5rem; }
                button { margin-top: 1rem; padding: 0.6rem 1rem; }
                pre { background: #f6f8fa; padding: 1rem; white-space: pre-wrap; }
            </style>
        </head>
        <body>
            <h1>Prompt Compiler</h1>
            <p>Compile and optimize prompts for better results.</p>
            <textarea id=\"prompt\" placeholder=\"Enter your prompt here\">Summarize the report and provide examples.</textarea>
            <button onclick=\"compilePrompt()\">Compile Prompt</button>
            <pre id=\"result\">Waiting for compilation...</pre>
            <script>
                async function compilePrompt() {
                    const prompt = document.getElementById('prompt').value;
                    const result = document.getElementById('result');
                    result.textContent = 'Compiling...';
                    const response = await fetch('/compile', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ content: prompt, context: { audience: 'executive' } })
                    });
                    const data = await response.json();
                    result.textContent = JSON.stringify(data, null, 2);
                }
            </script>
        </body>
        </html>
        """
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
