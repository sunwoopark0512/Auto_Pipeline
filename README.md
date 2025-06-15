# Auto Pipeline

This repository contains several scripts for generating marketing hooks, uploading
content to Notion, and retrying failed uploads. Environment variables should be
configured in a `.env` file based on `.env.example`.

## Key Environment Variables

- `OPENAI_API_KEY` – API key for OpenAI models
- `NOTION_API_TOKEN` – access token for Notion API
- `NOTION_HOOK_DB_ID` – Notion database for generated hooks
- `NOTION_KPI_DB_ID` – Notion database for KPI tracking
- `NOTION_DB_ID` – Notion database for keyword uploads
- `FAILED_ITEMS_PATH` – file path for storing any items that failed processing

See `.env.example` for the full list of variables and default values.
