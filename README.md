# Auto Pipeline

This repository contains Python scripts for generating marketing hooks and uploading them to Notion. Environment variables are loaded from a `.env` file. Copy `.env.example` to `.env` and adjust values before running any scripts.

## Key Environment Variables

- `OPENAI_API_KEY` – API key for OpenAI
- `NOTION_API_TOKEN` – access token for Notion
- `NOTION_DB_ID` – Notion database ID for keywords
- `NOTION_HOOK_DB_ID` – Notion database ID for generated hooks
- `NOTION_KPI_DB_ID` – Notion database for retry KPIs
- `FAILED_ITEMS_PATH` – path to store failed items across all scripts

See `.env.example` for the full list of configurable values.
