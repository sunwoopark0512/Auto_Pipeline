# Auto Pipeline

This repository contains an automated pipeline for collecting trending keywords, generating marketing hooks using GPT, and uploading the results to Notion. The process retries failed uploads and reports KPIs.

## Pipeline Stages

1. **Keyword Gathering** (`keyword_auto_pipeline.py`)
   - Collects keyword metrics from sources like Google Trends and Twitter.
   - Outputs filtered results to `KEYWORD_OUTPUT_PATH`.
2. **GPT Hook Generation** (`hook_generator.py`)
   - Reads the keyword JSON and generates short-form hooks using OpenAI.
   - Stores generated hooks in `HOOK_OUTPUT_PATH` and any failures in `FAILED_HOOK_PATH`.
3. **Notion Upload** (`notion_hook_uploader.py`)
   - Uploads generated hooks to a Notion database.
   - Skips duplicates and records failed uploads.
4. **Retry & KPI Dashboard** (`retry_failed_uploads.py`, `retry_dashboard_notifier.py`)
   - Retries failed uploads and logs results to a KPI dashboard in Notion.

`run_pipeline.py` ties these stages together and is invoked by the GitHub Actions workflow on a schedule.

## Environment Variables

The pipeline relies on several environment variables which can be provided via a `.env` file or the execution environment:

- `OPENAI_API_KEY` – API key for OpenAI GPT.
- `NOTION_API_TOKEN` – Notion integration token.
- `NOTION_HOOK_DB_ID` – Notion database ID for storing hooks.
- `NOTION_KPI_DB_ID` – Notion database ID for KPI logging.
- `NOTION_DB_ID` – Database ID used by the keyword uploader.
- `TOPIC_CHANNELS_PATH` – Path to the topics JSON file.
- `KEYWORD_OUTPUT_PATH` – Path for the keyword metrics output JSON.
- `HOOK_OUTPUT_PATH` – Path where generated hooks are saved.
- `FAILED_HOOK_PATH` – Path for GPT generation failures.
- `REPARSED_OUTPUT_PATH` – Path for failed uploads that were reparsed.
- `UPLOAD_DELAY` – Delay (seconds) between Notion uploads.
- `RETRY_DELAY` – Delay between retry attempts.
- `API_DELAY` – Delay between GPT API calls.
- `UPLOADED_CACHE_PATH` – Cache file of successfully uploaded keywords.
- `FAILED_UPLOADS_PATH` – File path storing failed keyword uploads.

## Installation

Install dependencies using:

```bash
pip install -r requirements.txt
```

## Running the Pipeline

To execute the pipeline manually, run:

```bash
python run_pipeline.py
```

A scheduled GitHub Actions workflow (`.github/workflows/daily-pipeline.yml.txt`) runs the same command daily.
