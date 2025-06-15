# Auto Pipeline

## Overview
This repository contains scripts that collect trending keywords, generate marketing hooks using OpenAI, and upload results to Notion. The process is orchestrated by `run_pipeline.py` and can also be scheduled through the provided GitHub Actions workflow.

## Main Scripts
- `keyword_auto_pipeline.py` – gathers keywords from Google Trends and Twitter.
- `hook_generator.py` – creates hook texts with the OpenAI API.
- `notion_hook_uploader.py` – uploads generated hooks to a Notion database.
- `retry_failed_uploads.py` – retries uploading items stored in failure logs.
- `retry_dashboard_notifier.py` – pushes retry KPI metrics to Notion.
- `run_pipeline.py` – entrypoint that executes the above scripts in sequence.

Scripts inside the `scripts/` folder provide additional upload utilities and retry logic.

## Required Environment Variables
Set the following variables in a `.env` file or in your shell environment before running the pipeline:

- `OPENAI_API_KEY` – API key for OpenAI.
- `NOTION_API_TOKEN` – token used to authenticate with Notion.
- `NOTION_HOOK_DB_ID` – target Notion database for hooks.
- `NOTION_DB_ID` – Notion database for keyword metrics.
- `NOTION_KPI_DB_ID` – database where retry KPI is stored.
- `KEYWORD_OUTPUT_PATH` – path to store collected keywords (default `data/keyword_output_with_cpc.json`).
- `HOOK_OUTPUT_PATH` – path for generated hooks file (default `data/generated_hooks.json`).
- `FAILED_HOOK_PATH` – log file for hooks that failed to upload.
- `REPARSED_OUTPUT_PATH` – retry summary JSON for KPI updates.
- `UPLOAD_DELAY`, `RETRY_DELAY`, `API_DELAY` – optional delays between API calls.

Other variables such as `TOPIC_CHANNELS_PATH`, `UPLOADED_CACHE_PATH`, `FAILED_UPLOADS_PATH`, or `SLACK_WEBHOOK_URL` may also be used in certain scripts.

## Usage
1. Create a `.env` file with the environment variables listed above.
2. Install dependencies (for example with `pip install -r requirements.txt`).
3. Run the pipeline:
   ```bash
   python run_pipeline.py
   ```

Results are written under the `data/` directory, and logs (including failure logs) are stored under `logs/`.

## GitHub Workflow
The repository includes `.github/workflows/daily-pipeline.yml.txt`, which runs the pipeline every day using the configured secrets. This workflow executes the same entrypoint and uploads any failure logs as artifacts.
