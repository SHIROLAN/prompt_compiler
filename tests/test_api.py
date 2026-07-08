from __future__ import annotations

from fastapi.testclient import TestClient

from prompt_compiler.api.main import app


client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root_endpoint_returns_web_ui() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "Prompt Compiler" in response.text
    assert "Compile Prompt" in response.text


def test_compile_endpoint_returns_optimized_prompt() -> None:
    response = client.post(
        "/compile",
        json={"content": "Summarize the report and provide examples.", "context": {"audience": "executive"}},
    )

    assert response.status_code == 200
    assert "optimized_prompt" in response.json()
    assert response.json()["original_prompt"] == "Summarize the report and provide examples."
    assert response.json()["optimized_prompt"] != response.json()["original_prompt"]
