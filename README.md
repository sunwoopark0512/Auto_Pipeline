# Auto_Pipeline

This repository contains scripts for generating marketing hooks and uploading them to Notion.

## Async hook generation

`hook_generator.py` now uses `asyncio` with OpenAI's async API. Multiple keywords are processed concurrently while respecting rate limits.

Environment variables:

- `OPENAI_API_KEY` – your OpenAI key.
- `API_DELAY` – delay between API calls (seconds, default `1.0`).
- `MAX_CONCURRENT` – maximum concurrent API requests (default `3`).

Run:

```bash
python hook_generator.py
```

The behaviour is the same but generation is faster thanks to concurrency.
