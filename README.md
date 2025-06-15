# Auto Pipeline

This repository contains scripts for generating marketing hooks and uploading them to Notion. The pipeline relies on several environment variables that should be defined in a `.env` file.

## Environment Variables

- `OPENAI_API_KEY` – API key for OpenAI
- `NOTION_API_TOKEN` – API token for Notion
- `NOTION_HOOK_DB_ID` – Target database ID for hooks
- `NOTION_DB_ID` – Target database ID for keywords
- `NOTION_KPI_DB_ID` – Target database ID for KPI statistics
- `FAILED_ITEMS_PATH` – Path for storing failed item logs (each script provides its own default)

Copy `.env.example` to `.env` and fill in the values before running any script.
