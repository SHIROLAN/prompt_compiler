from __future__ import annotations

from prompt_compiler.compiler.contracts import Scorer
from prompt_compiler.models.prompt_models import Prompt, PromptScore


class HeuristicScorer(Scorer):
    """A deterministic scorer based on prompt content heuristics."""

    def score(self, prompt: Prompt) -> PromptScore:
        """Score a prompt using lightweight heuristics."""
        text = prompt.content.lower()
        clarity = 0.8 if len(text.split()) >= 4 else 0.6
        specificity = 0.75 if any(token in text for token in ("specific", "detailed", "exactly", "clearly")) else 0.5
        completeness = 0.7 if any(token in text for token in ("context", "format", "tone", "audience")) else 0.45
        overall = (clarity + specificity + completeness) / 3
        return PromptScore(clarity=clarity, specificity=specificity, completeness=completeness, overall=overall)
