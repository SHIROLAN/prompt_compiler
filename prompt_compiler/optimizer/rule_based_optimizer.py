from __future__ import annotations

from prompt_compiler.compiler.contracts import Optimizer
from prompt_compiler.models.prompt_models import Prompt, PromptAnalysis


class RuleBasedOptimizer(Optimizer):
    """A deterministic optimizer that rewrites prompts for clarity and completeness."""

    def optimize(self, prompt: Prompt, analysis: PromptAnalysis) -> Prompt:
        """Return an optimized prompt based on the analysis context."""
        content = prompt.content.strip()
        if not content:
            return prompt

        rewritten = self._rewrite_prompt(content, analysis)
        return Prompt(
            id=prompt.id,
            content=rewritten,
            context=prompt.context,
            version=prompt.version,
        )

    def _rewrite_prompt(self, content: str, analysis: PromptAnalysis) -> str:
        normalized = content.rstrip("? .")
        base = f"You are helping with {analysis.intent.category.value if analysis.intent else 'the requested task'}."
        if analysis.intent and analysis.intent.category.value == "summarization":
            rewritten = f"{base} Summarize the following content clearly and concisely."
        elif analysis.intent and analysis.intent.category.value == "classification":
            rewritten = f"{base} Classify the input into the most appropriate category and explain briefly."
        else:
            rewritten = f"{base} Respond clearly, directly, and with the necessary context."

        if analysis.concerns:
            rewritten += " Include any relevant context and avoid ambiguity."

        if analysis.detected_techniques:
            rewritten += " Follow the requested structure and examples when provided."

        return f"{rewritten} Original request: {normalized}."
