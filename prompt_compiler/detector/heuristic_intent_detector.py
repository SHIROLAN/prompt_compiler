from __future__ import annotations

from prompt_compiler.compiler.contracts import IntentDetector
from prompt_compiler.models.prompt_models import Prompt


class HeuristicIntentDetector(IntentDetector):
    """A simple intent detector based on keyword matching."""

    def detect(self, prompt: Prompt) -> str:
        """Return a normalized intent label for the prompt."""
        text = prompt.content.lower()
        if any(keyword in text for keyword in ("summarize", "summary", "tl;dr")):
            return "summarization"
        if any(keyword in text for keyword in ("classify", "category", "label")):
            return "classification"
        if any(keyword in text for keyword in ("write", "draft", "generate", "create")):
            return "generation"
        if any(keyword in text for keyword in ("extract", "find", "identify")):
            return "extraction"
        return "general"
