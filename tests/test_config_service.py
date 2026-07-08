from __future__ import annotations

from prompt_compiler.config.settings import CompilerSettings, get_settings
from prompt_compiler.models.prompt_models import Prompt
from prompt_compiler.services.compiler_service import CompilerService


def test_get_settings_reads_environment_defaults(monkeypatch) -> None:
    monkeypatch.setenv("PROMPT_COMPILER_MAX_TOKENS", "240")
    monkeypatch.setenv("PROMPT_COMPILER_PREFERRED_TOKENS", "120")

    settings = get_settings()

    assert settings.max_tokens == 240
    assert settings.preferred_tokens == 120


def test_compiler_service_uses_settings_for_token_budget() -> None:
    settings = CompilerSettings(max_tokens=90, preferred_tokens=60)
    service = CompilerService(settings=settings)

    optimizer = service._compiler._optimizer
    assert optimizer._budget.max_tokens == 90
    assert optimizer._budget.preferred_tokens == 60


def test_compiler_service_compiles_prompt() -> None:
    service = CompilerService()
    result = service.compile_prompt("Summarize the report clearly.")

    assert result.original_prompt.content == "Summarize the report clearly."
    assert result.optimized_prompt.content != result.original_prompt.content
    assert result.score_after.overall >= 0.0
