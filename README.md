# Auto Pipeline

This repository contains scripts for collecting trending keywords, generating marketing hooks using OpenAI, and uploading the results to Notion. Environment variables control API keys, database IDs and file paths.

## Environment Variables
See `.env.example` for default values. Important variables include:

- `OPENAI_API_KEY` – API key for OpenAI
- `NOTION_API_TOKEN` – Notion integration token
- `NOTION_HOOK_DB_ID` – ID of the Notion database for hooks
- `NOTION_DB_ID` – ID of the Notion database for keywords
- `NOTION_KPI_DB_ID` – ID of the Notion database for KPI tracking
- `KEYWORD_OUTPUT_PATH` – path for keyword collection output
- `HOOK_OUTPUT_PATH` – path for generated hooks
- `FAILED_HOOK_PATH` – file for failed hook generation results
- `REPARSED_OUTPUT_PATH` – file for failed uploads after reparsing
- `UPLOADED_CACHE_PATH` – cache file for successfully uploaded keywords
- `UPLOAD_DELAY`, `API_DELAY`, `RETRY_DELAY` – timing configurations

Configure these variables in an `.env` file before running the pipeline.
