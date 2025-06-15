# Auto Pipeline

This repository contains a collection of scripts that automate the process of gathering trending keywords, generating marketing copy using OpenAI, and uploading the results to Notion. The pipeline can be run end‑to‑end with a single command once the required environment variables are configured.

## Setup

1. Install Python 3.10 or later.
2. Install the dependencies:
   ```bash
   pip install openai notion-client python-dotenv pytrends snscrape
   ```
3. Create a `.env` file in the project root (or export the variables in your environment) with the following values.

## Required Environment Variables

- `OPENAI_API_KEY` – API key for OpenAI.
- `NOTION_API_TOKEN` – Notion integration token used by uploader scripts.
- `NOTION_DB_ID` – Database ID for keyword metrics (used by `scripts/notion_uploader.py`).
- `NOTION_HOOK_DB_ID` – Database ID where generated hooks are stored.
- `NOTION_KPI_DB_ID` – Database ID for logging retry statistics.
- `KEYWORD_OUTPUT_PATH` – Path to save keyword collection results (defaults to `data/keyword_output_with_cpc.json`).
- `HOOK_OUTPUT_PATH` – Path where generated hooks are written.
- `FAILED_HOOK_PATH` – File storing failed hook generations.
- `UPLOADED_CACHE_PATH` – Cache file of already uploaded keywords.
- `FAILED_UPLOADS_PATH` – File recording failed keyword uploads.
- `REPARSED_OUTPUT_PATH` – JSON file containing items that failed and were reparsed.
- `UPLOAD_DELAY` – Delay in seconds between Notion uploads.
- `RETRY_DELAY` – Delay in seconds between retry attempts.
- `API_DELAY` – Delay between OpenAI API calls.
- `TOPIC_CHANNELS_PATH` – Path to the topic configuration JSON (`config/topic_channels.json`).

Only the variables relevant to the scripts you run are required.

## Running the Pipeline

Execute all steps in sequence using:

```bash
python run_pipeline.py
```

The script runs a series of helper scripts listed in `PIPELINE_SEQUENCE` and logs progress to the console.

## Script Overview

- **`keyword_auto_pipeline.py`** – Fetches trending keywords from Google Trends and Twitter and writes the filtered results to `KEYWORD_OUTPUT_PATH`.
- **`hook_generator.py`** – Uses OpenAI to create hook sentences, blog drafts and video titles for each keyword from the previous step. Outputs JSON to `HOOK_OUTPUT_PATH`.
- **`notion_hook_uploader.py`** – Uploads generated hooks from `HOOK_OUTPUT_PATH` to the Notion database specified by `NOTION_HOOK_DB_ID`.
- **`scripts/notion_uploader.py`** – Uploads raw keyword metrics to the Notion database given by `NOTION_DB_ID`.
- **`retry_failed_uploads.py`** / **`scripts/retry_failed_uploads.py`** – Attempts to re‑upload items that previously failed and records the outcome.
- **`retry_dashboard_notifier.py`** – Summarises retry results and writes KPI data to the Notion dashboard defined by `NOTION_KPI_DB_ID`.
- **`run_pipeline.py`** – Main entry point that orchestrates the steps above.

Adjust the configuration paths in your `.env` file as needed before running the pipeline.
