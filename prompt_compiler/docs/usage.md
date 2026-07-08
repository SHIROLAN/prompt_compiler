# Usage Guide

## CLI Usage

Run the compiler directly:

```bash
python -m prompt_compiler.cli "Write a concise product launch announcement."
```

The command prints:
- the original prompt
- the optimized prompt
- detected intent
- selected techniques
- the final score

## HTTP API Usage

Start the server:

```bash
uvicorn prompt_compiler.api.main:app --reload
```

Send a compile request:

```bash
curl -X POST http://127.0.0.1:8000/compile \
  -H "Content-Type: application/json" \
  -d '{"content": "Summarize the quarterly results for a non-technical audience.", "context": {"audience": "executive"}}'
```

You should receive a JSON response containing the optimized prompt, intent, techniques, scores, and notes.
