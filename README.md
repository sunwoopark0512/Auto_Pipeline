# Auto Pipeline

## Overview
This repository contains a simple automated pipeline that collects trending keywords, generates marketing hooks using GPT, and uploads them to Notion. The main stages are:

1. **Keyword collection** – `keyword_auto_pipeline.py` gathers trending search terms from Google Trends and Twitter.
2. **GPT hook generation** – `hook_generator.py` creates hook lines, blog paragraph drafts and video titles for each keyword using OpenAI.
3. **Notion upload & retry** – `notion_hook_uploader.py` uploads the generated hooks to a Notion database. Failed uploads are retried by `retry_failed_uploads.py` and metrics are pushed via `retry_dashboard_notifier.py`.

The scripts can be executed sequentially through `run_pipeline.py` or individually.

## Environment Variables
Set the following variables (commonly via a `.env` file) before running the pipeline:

- `OPENAI_API_KEY` – API key for OpenAI.
- `NOTION_API_TOKEN` – Notion integration token.
- `NOTION_HOOK_DB_ID` – Notion database ID for hook uploads.
- `NOTION_KPI_DB_ID` – Database ID for logging retry statistics.
- `NOTION_DB_ID` – (for `notion_uploader.py`) keyword upload database.
- `TOPIC_CHANNELS_PATH` – path to `topic_channels.json`.
- `KEYWORD_OUTPUT_PATH` – path for collected keyword JSON.
- `HOOK_OUTPUT_PATH` – path for generated hook data.
- `FAILED_HOOK_PATH` – file for hooks that failed to generate or upload.
- `UPLOADED_CACHE_PATH` – cache for successfully uploaded keywords.
- `FAILED_UPLOADS_PATH` – log for keyword uploads that failed.
- `REPARSED_OUTPUT_PATH` – path used when reprocessing failed keywords.
- `UPLOAD_DELAY` – delay (seconds) between Notion uploads.
- `RETRY_DELAY` – delay (seconds) between retry attempts.
- `API_DELAY` – delay between OpenAI API calls.

## Installation
Install the required packages using `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Running Manually
Execute the entire pipeline locally by running:

```bash
python run_pipeline.py
```

This runs the scripts in order and logs progress to the console (and `logs/` where applicable).

## Scheduled Workflow
A daily GitHub Actions workflow (`.github/workflows/daily-pipeline.yml.txt`) runs the same pipeline automatically. Failed keywords are uploaded as workflow artifacts and a short summary is appended to the workflow run summary.


