# Auto Pipeline

This repository contains scripts for generating marketing hooks and managing Notion uploads.

## Environment Variables

The following variables control path locations and credentials. Copy `.env.example` to `.env` and fill in your values.

- `OPENAI_API_KEY` – API key for OpenAI.
- `NOTION_API_TOKEN` – Notion API token.
- `NOTION_HOOK_DB_ID` – Database ID for generated hooks.
- `NOTION_KPI_DB_ID` – KPI database ID.
- `NOTION_DB_ID` – Keyword database ID.
- `HOOK_OUTPUT_PATH` – Generated hook JSON output.
- `KEYWORD_OUTPUT_PATH` – Keyword output file.
- `FAILED_GENERATION_PATH` – Path for failed hook generation items.
- `FAILED_UPLOAD_PATH` – Path for failed Notion uploads.
- `FAILED_RETRY_PATH` – Path for items still failed after retries.
- `UPLOAD_DELAY` – Delay between Notion uploads.
- `RETRY_DELAY` – Delay between retry attempts.
- `API_DELAY` – Delay between OpenAI calls.
- `UPLOADED_CACHE_PATH` – Cache file for uploaded keywords.
- `TOPIC_CHANNELS_PATH` – Configuration for topic channels.


