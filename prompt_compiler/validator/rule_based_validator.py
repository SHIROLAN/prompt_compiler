from __future__ import annotations

from prompt_compiler.compiler.contracts import Validator
from prompt_compiler.models.prompt_models import Prompt


class RuleBasedValidator(Validator):
    """A validator enforcing a small set of structural prompt rules."""

    def validate(self, prompt: Prompt) -> bool:
        """Return True when the prompt satisfies the validation rules."""
        if not prompt.content.strip():
            return False
        if len(prompt.content.split()) < 4:
            return False
        if prompt.content.count("?") > 2:
            return False
        return True
