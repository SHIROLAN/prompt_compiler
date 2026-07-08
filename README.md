# Prompt Compiler

Prompt Compiler is a modular, extensible prompt optimization service. It analyzes prompts, detects intent, selects techniques, optimizes them for clarity and token efficiency, validates them, and scores the result.

## Features

- Intent analysis
- Prompt technique selection
- Token-aware optimization
- Prompt validation
- HTTP API access
- CLI access

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

### HTTP API

Start the API with:

```bash
uvicorn prompt_compiler.api.main:app --reload
```

Then send a request:

```bash
curl -X POST http://127.0.0.1:8000/compile \
  -H "Content-Type: application/json" \
  -d '{"content": "Summarize the report clearly for an executive audience.", "context": {"audience": "executive"}}'
```

## Web App Deployment

This project now exposes a simple browser UI at the root route and a JSON API at `/compile`, which makes it suitable for deployment as a lightweight web application.

### Run locally

```bash
uvicorn prompt_compiler.api.main:app --host 0.0.0.0 --port 8000
```

Then open http://127.0.0.1:8000/ in your browser.

### Deploy to Google Cloud Run

1. Create a Google Cloud project.
2. Enable Cloud Run API.
3. Build and deploy the app with:

```bash
gcloud run deploy prompt-compiler --source . --region us-central1 --allow-unauthenticated
```

This will publish your app as a public web service that can be used from a browser or embedded into other apps.

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
