from __future__ import annotations

from typer.testing import CliRunner

from prompt_compiler.cli import app


runner = CliRunner()


def test_cli_prints_compiled_output() -> None:
    result = runner.invoke(app, ["Summarize the report clearly."])

    assert result.exit_code == 0
    assert "Original:" in result.stdout
    assert "Optimized:" in result.stdout
