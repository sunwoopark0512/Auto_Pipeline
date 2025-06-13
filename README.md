# Auto Pipeline

This repository contains a collection of scripts that generate marketing hooks, upload them to Notion and track retry statistics.  The pipeline is designed to run daily via GitHub Actions.

## Pipeline Overview
1. **keyword_auto_pipeline.py** – collects trending keywords from Google Trends and Twitter.
2. **hook_generator.py** – uses OpenAI to create marketing hooks for each keyword.
3. **notion_hook_uploader.py** – uploads generated hooks to the configured Notion database.
4. **retry_failed_uploads.py** – retries uploading hooks that previously failed.
5. **retry_dashboard_notifier.py** – posts a summary of retry results to a Notion dashboard.

The entry point `run_pipeline.py` sequentially executes these scripts.

## Required Environment Variables
- `OPENAI_API_KEY`
- `NOTION_API_TOKEN`
- `NOTION_HOOK_DB_ID`
- `NOTION_KPI_DB_ID`
- `NOTION_DB_ID` (for keyword uploads)
- `REPARSED_OUTPUT_PATH`
- `FAILED_HOOK_PATH`
- `KEYWORD_OUTPUT_PATH`

Create a `.env` file with these variables for local execution.

## Running Locally
```bash
pip install -r requirements.txt
python run_pipeline.py
```

## GitHub Actions
The workflow in `.github/workflows/daily-pipeline.yml` runs the pipeline daily. Secrets matching the environment variables above must be configured in your repository settings.
