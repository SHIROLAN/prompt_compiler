# Prompt Compiler

Prompt Compiler is a modular, extensible prompt optimization service. It analyzes prompts, detects intent, selects techniques, optimizes them for clarity and token efficiency, validates them, and scores the result. The package now also exposes a simple browser-based web UI and a CLI entry point that works correctly after installation.

## Features

- Intent analysis
- Prompt technique selection
- Token-aware optimization
- Prompt validation and scoring
- Browser-based web UI
- HTTP API access
- CLI access

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Quick Start

### CLI

Run the compiler from the command line:

```bash
python -m prompt_compiler.cli "Summarize the report clearly for an executive audience."
```

Or, after installing the package:

```bash
prompt-compiler "Summarize the report clearly for an executive audience."
```

Expected output includes the original prompt, optimized prompt, detected intent, selected techniques, and a score.

### Web App

Start the web application with:

```bash
uvicorn prompt_compiler.api.main:app --host 0.0.0.0 --port 8000
```

Then open http://127.0.0.1:8000/ in your browser. The root page provides a simple UI for compiling prompts, and `/compile` accepts JSON requests for programmatic use. The app uses the shared compiler service so environment-based settings are honored in both the web UI and the API.

### HTTP API

Send a request to the API with:

```bash
curl -X POST http://127.0.0.1:8000/compile \
  -H "Content-Type: application/json" \
  -d '{"content": "Summarize the report clearly for an executive audience.", "context": {"audience": "executive"}}'
```

## Deployment

This project is suitable for deployment as a lightweight web application or API. A common option is Google Cloud Run.

### Deploy to Google Cloud Run

1. Create or select a Google Cloud project.
2. Enable the Cloud Run API.
3. Deploy the app with:

```bash
gcloud run deploy prompt-compiler --source . --region us-central1 --allow-unauthenticated
```

This publishes the service as a public web endpoint that can be opened in a browser or integrated into other applications.

## Configuration

The compiler reads environment variables for configuration:

- PROMPT_COMPILER_MAX_TOKENS
- PROMPT_COMPILER_PREFERRED_TOKENS
- PROMPT_COMPILER_ENABLE_TOKEN_AWARE_OPTIMIZATION
- PROMPT_COMPILER_ENABLE_VALIDATION

Example:

```bash
export PROMPT_COMPILER_MAX_TOKENS=180
export PROMPT_COMPILER_PREFERRED_TOKENS=100
export PROMPT_COMPILER_ENABLE_TOKEN_AWARE_OPTIMIZATION=true
export PROMPT_COMPILER_ENABLE_VALIDATION=true
```

## Project Structure

- prompt_compiler/analyzer: prompt analysis implementations
- prompt_compiler/compiler: orchestration and contracts
- prompt_compiler/detector: intent detection implementations
- prompt_compiler/optimizer: prompt optimization strategies
- prompt_compiler/scorer: prompt scoring implementations
- prompt_compiler/techniques: technique selection strategies
- prompt_compiler/tokenizer: token budget abstractions
- prompt_compiler/validator: validation implementations
- prompt_compiler/api: FastAPI app and schemas
- prompt_compiler/config: configuration settings
- prompt_compiler/services: application services
