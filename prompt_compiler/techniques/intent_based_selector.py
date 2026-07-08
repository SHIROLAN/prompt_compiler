from __future__ import annotations

from prompt_compiler.compiler.contracts import TechniqueSelector
from prompt_compiler.models.prompt_models import Prompt, PromptAnalysis, Technique, TechniqueKind


class IntentBasedTechniqueSelector(TechniqueSelector):
    """Select prompt-engineering techniques based on detected intent and content."""

    def select(self, prompt: Prompt, analysis: PromptAnalysis) -> list[str]:
        """Return a list of technique identifiers for the prompt."""
        text = prompt.content.lower()
        techniques: list[str] = []

        if analysis.intent is not None:
            if analysis.intent.category.value == "summarization":
                techniques.append(TechniqueKind.CHAIN_OF_THOUGHT.value)
            if "example" in text or "examples" in text:
                techniques.append(TechniqueKind.FEW_SHOT.value)
            if "act as" in text or "role" in text:
                techniques.append(TechniqueKind.ROLE_PROMPTING.value)

        if analysis.concerns and len(analysis.concerns) > 0:
            techniques.append(TechniqueKind.SELF_CRITIQUE.value)

        return techniques
