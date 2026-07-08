from __future__ import annotations

from prompt_compiler.compiler.contracts import Optimizer
from prompt_compiler.models.prompt_models import Prompt, PromptAnalysis
from prompt_compiler.tokenizer.token_budget import TokenBudget


class TokenAwareOptimizer(Optimizer):
    """An optimizer that rewrites prompts while respecting a token budget."""

    def __init__(self, budget: TokenBudget | None = None) -> None:
        self._budget = budget or TokenBudget()

    def optimize(self, prompt: Prompt, analysis: PromptAnalysis) -> Prompt:
        """Return an optimized prompt tuned for the configured token budget."""
        content = prompt.content.strip()
        if not content:
            return prompt

        rewritten = self._rewrite_with_budget(content, analysis)
        return Prompt(
            id=prompt.id,
            content=rewritten,
            context=prompt.context,
            version=prompt.version,
        )

    def _rewrite_with_budget(self, content: str, analysis: PromptAnalysis) -> str:
        base = f"You are helping with {analysis.intent.category.value if analysis.intent else 'the requested task'}."
        directive = self._directive_for_analysis(analysis)
        concise = f"{base} {directive}"

        words = concise.split()
        if len(words) > self._budget.preferred_tokens // 2:
            concise = " ".join(words[: self._budget.preferred_tokens // 2])

        return f"{concise} Keep the response concise and within a {self._budget.max_tokens}-token budget. Original request: {content}."

    def _directive_for_analysis(self, analysis: PromptAnalysis) -> str:
        if analysis.intent and analysis.intent.category.value == "summarization":
            return "Summarize the content clearly and concisely."
        if analysis.intent and analysis.intent.category.value == "classification":
            return "Classify the input into the most appropriate category."
        if analysis.detected_techniques:
            return "Follow the selected techniques and provide the requested structure."
        return "Respond clearly, directly, and with the necessary context."
