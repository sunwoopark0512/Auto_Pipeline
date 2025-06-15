# Auto Pipeline

This repository contains scripts that generate marketing hooks and upload them to Notion. Environment variables can be defined in a `.env` file or via the environment.

## Key Environment Variables

- `NOTION_API_TOKEN` – token used to access the Notion API.
- `NOTION_DB_ID` – ID of the keywords database.
- `NOTION_HOOK_DB_ID` – ID of the hooks database.
- `OPENAI_API_KEY` – API key for OpenAI calls.
- `FAILED_ITEMS_PATH` – path used by all scripts to store items that failed during processing. Defaults to `logs/failed_items.json`.

Copy `.env.example` to `.env` and fill in your values before running the pipeline.
