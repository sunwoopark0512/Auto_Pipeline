# Auto Pipeline

This repository contains scripts for generating trending keywords using Google Trends and Twitter data, creating marketing hooks with OpenAI GPT, and uploading the results to Notion.

## Environment Variables

Create a `.env` file in the project root with the following variables:

- `OPENAI_API_KEY` – API key for OpenAI GPT.
- `NOTION_API_TOKEN` – token for Notion API access.
- `NOTION_HOOK_DB_ID` – ID of the Notion database for generated hooks.
- `NOTION_KPI_DB_ID` – ID of the Notion database for KPI stats.
- `NOTION_DB_ID` – ID of the Notion database for keyword uploads (used in `scripts/notion_uploader.py`).
- `TOPIC_CHANNELS_PATH` – optional path to `config/topic_channels.json`.
- `KEYWORD_OUTPUT_PATH` – output path for keywords JSON (default `data/keyword_output_with_cpc.json`).
- `HOOK_OUTPUT_PATH` – output path for generated hooks (default `data/generated_hooks.json`).
- `FAILED_HOOK_PATH` – file used to log failed hook generation attempts.
- `REPARSED_OUTPUT_PATH` – file path for reparsed failed items.
- `UPLOADED_CACHE_PATH` – cache file for uploaded keywords.
- `FAILED_UPLOADS_PATH` – file path for failed keyword uploads.
- `UPLOAD_DELAY` – delay between Notion upload requests (seconds).
- `API_DELAY` – delay between OpenAI API requests (seconds).
- `RETRY_DELAY` – delay between retry attempts (seconds).

## Installation

Install the required Python packages:

```bash
pip install openai python-dotenv notion-client pytrends snscrape
```

## Workflow

1. **Keyword collection** – `keyword_auto_pipeline.py` gathers trending keywords from Google Trends and Twitter and saves them to the file defined by `KEYWORD_OUTPUT_PATH`.
2. **Hook generation** – `hook_generator.py` reads the keyword file and uses OpenAI GPT to generate hook sentences and related content. Results are stored in `HOOK_OUTPUT_PATH`.
3. **Upload to Notion** – `notion_hook_uploader.py` uploads generated hooks to the Notion database identified by `NOTION_HOOK_DB_ID`.
4. **Retry uploads** – `retry_failed_uploads.py` looks for failed items (path given by `REPARSED_OUTPUT_PATH`) and retries uploading them to Notion.
5. **Dashboard update** – `retry_dashboard_notifier.py` reads the retry results and writes KPI metrics to the database specified in `NOTION_KPI_DB_ID`.
6. **Full pipeline** – run `run_pipeline.py` to execute the above scripts in sequence.

Each script can be run individually with Python:

```bash
python keyword_auto_pipeline.py
python hook_generator.py
python notion_hook_uploader.py
python retry_failed_uploads.py
python retry_dashboard_notifier.py
```

Or run the entire process:

```bash
python run_pipeline.py
```

