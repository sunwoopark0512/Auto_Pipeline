# Auto Pipeline

This repository automates collecting trending keywords, generating marketing hooks using GPT, and uploading results to Notion. The main pipeline is executed daily through a GitHub Actions workflow and can also be run locally.

## Project Overview
1. **Keyword Collection** – `keyword_auto_pipeline.py` gathers keywords from Google Trends and Twitter.
2. **GPT Hook Generation** – `hook_generator.py` uses the keywords to create hook ideas via OpenAI.
3. **Notion Uploads** – `notion_hook_uploader.py` (and related scripts) upload generated hooks to Notion databases.
4. **Retry & KPI Tracking** – failed uploads are retried with `retry_failed_uploads.py` and statistics are pushed to a KPI dashboard with `retry_dashboard_notifier.py`.

## Required Environment Variables
The pipeline relies on multiple environment variables which may be provided through a `.env` file or the execution environment:

- `OPENAI_API_KEY` – OpenAI API key.
- `NOTION_API_TOKEN` – token for the Notion client.
- `NOTION_DB_ID` – Notion database ID for raw keywords.
- `NOTION_HOOK_DB_ID` – Notion database ID for generated hooks.
- `NOTION_KPI_DB_ID` – Notion database ID for KPI tracking.
- `TOPIC_CHANNELS_PATH` – path to the topic configuration JSON.
- `KEYWORD_OUTPUT_PATH` – file path where keywords are stored.
- `HOOK_OUTPUT_PATH` – file path for generated hooks.
- `FAILED_HOOK_PATH` – path for hooks that failed to parse.
- `REPARSED_OUTPUT_PATH` – file used when retrying failed uploads.
- `UPLOADED_CACHE_PATH` – cache file of successfully uploaded keywords.
- `FAILED_UPLOADS_PATH` – log file for Notion upload failures.
- `UPLOAD_DELAY` – delay between Notion page creations.
- `RETRY_DELAY` – delay between retry attempts.
- `API_DELAY` – wait time between OpenAI API calls.

## Installation
Install the required packages:

```bash
pip install -r requirements.txt
```

## Running the Pipeline
To run the entire pipeline manually:

```bash
python run_pipeline.py
```

A daily workflow defined in `.github/workflows/daily-pipeline.yml.txt` runs the same entry point on GitHub Actions to keep hooks up to date.
