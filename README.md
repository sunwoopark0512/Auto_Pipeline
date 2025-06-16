# Auto Pipeline

This repository contains a collection of scripts that generate trending keywords, create marketing hooks using OpenAI and upload the results to Notion.

## Setup
1. Install Python 3.10 or later.
2. Install the required packages:
   ```bash
   pip install openai notion-client python-dotenv pytrends snscrape
   ```
3. Create a `.env` file based on `.env.example` and fill in your API keys and optional settings.

## Usage
The main workflow consists of three steps and can be executed manually:

1. **Generate keywords**
   ```bash
   python keyword_auto_pipeline.py
   ```
   This produces a JSON file defined by `KEYWORD_OUTPUT_PATH` (default: `data/keyword_output_with_cpc.json`).

2. **Generate hooks from the keywords**
   ```bash
   python hook_generator.py
   ```
   The script reads keywords from `KEYWORD_OUTPUT_PATH` and writes hook results to `HOOK_OUTPUT_PATH` (default: `data/generated_hooks.json`).
   `OPENAI_API_KEY` must be set for this step.

3. **Upload hooks to Notion**
   ```bash
   python notion_hook_uploader.py
   ```
   The file defined by `HOOK_OUTPUT_PATH` is uploaded to the Notion database specified by `NOTION_HOOK_DB_ID`.

Optional scripts such as `retry_failed_uploads.py` and `retry_dashboard_notifier.py` can be used to retry failed uploads and log KPI metrics.

## Environment Variables
Environment variables are loaded via `python-dotenv`. The main ones are:

- `OPENAI_API_KEY` – API key used by `hook_generator.py`.
- `NOTION_API_TOKEN` – token for the Notion client.
- `NOTION_HOOK_DB_ID` – database ID used by `notion_hook_uploader.py`.
- `NOTION_DB_ID` – database ID for `scripts/notion_uploader.py`.
- `NOTION_KPI_DB_ID` – KPI dashboard used by `retry_dashboard_notifier.py`.
- `KEYWORD_OUTPUT_PATH` – path for keyword JSON output.
- `HOOK_OUTPUT_PATH` – path for generated hook JSON.
- `FAILED_HOOK_PATH` – storage for failed hook generations.
- `FAILED_UPLOADS_PATH` – storage for failed Notion uploads.
- `UPLOADED_CACHE_PATH` – cache for successfully uploaded keywords.
- `REPARSED_OUTPUT_PATH` – file used when retrying failed uploads.
- `API_DELAY`, `UPLOAD_DELAY`, `RETRY_DELAY` – delays between API calls.
- `TOPIC_CHANNELS_PATH` – location of topic configuration JSON.

All of these variables may be defined in a `.env` file so they are automatically loaded when running the scripts.

