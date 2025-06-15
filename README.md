# Auto Pipeline

This repository contains a small pipeline for collecting trending keywords, generating hook sentences with OpenAI and uploading them to Notion.

## Setup

1. Install Python 3.10 or later.
2. Install dependencies (see `requirements.txt` if present):
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file based on `.env.example` and fill in the required secrets.

## Environment Variables

The following variables are used across the scripts:

- `OPENAI_API_KEY` – API key for OpenAI.
- `NOTION_API_TOKEN` – Notion integration token.
- `NOTION_DB_ID` – Database ID for uploading keywords (scripts/notion_uploader.py).
- `NOTION_HOOK_DB_ID` – Database ID for generated hooks.
- `NOTION_KPI_DB_ID` – Database ID for KPI metrics.
- `SLACK_WEBHOOK_URL` – Slack webhook used in the GitHub Actions workflow.
- `TOPIC_CHANNELS_PATH` – Path to `topic_channels.json` (defaults to `config/topic_channels.json`).
- `KEYWORD_OUTPUT_PATH` – Output path for collected keywords (`data/keyword_output_with_cpc.json`).
- `HOOK_OUTPUT_PATH` – JSON file for generated hooks (`data/generated_hooks.json`).
- `FAILED_HOOK_PATH` – File used to log failed hook generations (`logs/failed_hooks.json`).
- `UPLOAD_DELAY` – Delay between Notion uploads (seconds).
- `API_DELAY` – Delay between OpenAI API calls (seconds).
- `UPLOADED_CACHE_PATH` – Cache file for already uploaded keywords.
- `FAILED_UPLOADS_PATH` – Location to store failed Notion uploads.
- `REPARSED_OUTPUT_PATH` – File for reparsed failed keywords.
- `RETRY_DELAY` – Delay between retry uploads.

## Running the Scripts

1. **Collect keywords**
   ```bash
   python keyword_auto_pipeline.py
   ```
   Creates a keyword JSON file at `KEYWORD_OUTPUT_PATH`.

2. **Generate hooks**
   ```bash
   python hook_generator.py
   ```
   Reads the keyword JSON and writes generated hooks to `HOOK_OUTPUT_PATH`.

3. **Upload to Notion**
   ```bash
   python notion_hook_uploader.py
   ```
   Uploads hooks to the database specified by `NOTION_HOOK_DB_ID`.

## GitHub Actions Workflow

The repository includes `.github/workflows/daily-pipeline.yml.txt` which runs the pipeline daily via a scheduled GitHub Actions workflow. The workflow installs dependencies, executes `scripts/run_pipeline.py`, and uploads a summary artifact containing any failed keywords. Secrets such as `OPENAI_API_KEY`, `NOTION_API_TOKEN` and others must be configured in the repository settings for the workflow to function.

