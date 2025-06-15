# Auto Pipeline

This repository contains a collection of scripts that gather trending keywords, generate marketing hooks using OpenAI GPT models and upload them to Notion. The scripts can be executed individually or run together through the provided pipeline.

## Setup

1. Install Python 3.10 or newer.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root with the required environment variables (see below).

## Environment Variables

The scripts rely on several environment variables. Default values are shown in parentheses where applicable.

- `OPENAI_API_KEY` – API key for OpenAI.
- `NOTION_API_TOKEN` – Notion integration token.
- `NOTION_DB_ID` – Target Notion database for keyword records.
- `NOTION_HOOK_DB_ID` – Database ID used to store generated hooks.
- `NOTION_KPI_DB_ID` – Database ID for KPI metrics.
- `KEYWORD_OUTPUT_PATH` (`data/keyword_output_with_cpc.json`)
- `HOOK_OUTPUT_PATH` (`data/generated_hooks.json`)
- `FAILED_HOOK_PATH` (`logs/failed_hooks.json`)
- `FAILED_UPLOADS_PATH` (`logs/failed_uploads.json`)
- `REPARSED_OUTPUT_PATH` (`logs/failed_keywords_reparsed.json`)
- `UPLOADED_CACHE_PATH` (`data/uploaded_keywords_cache.json`)
- `TOPIC_CHANNELS_PATH` (`config/topic_channels.json`)
- `API_DELAY` – Delay between OpenAI API calls in seconds (default `1.0`).
- `UPLOAD_DELAY` – Delay between Notion uploads in seconds (default `0.5`).
- `RETRY_DELAY` – Delay used by retry scripts (default `0.5`).

## Usage

Run scripts individually as needed or execute `run_pipeline.py` to run all steps in sequence:

```bash
python run_pipeline.py
```

Main scripts include:

- `keyword_auto_pipeline.py` – collects trending keywords from Google Trends and Twitter.
- `hook_generator.py` – generates hook sentences with GPT based on collected keywords.
- `notion_hook_uploader.py` – uploads generated hooks to a Notion database.
- `retry_failed_uploads.py` – retries failed Notion uploads.
- `retry_dashboard_notifier.py` – posts KPI summaries to Notion.

Logs and intermediate data are stored in the paths configured through environment variables.
