# Auto Pipeline

This repository contains a collection of scripts used to gather trending keywords, generate marketing hooks with GPT, and upload the results to Notion.  The pipeline is designed to run either manually or via the provided GitHub Actions workflow.

## Installation

1. Create a Python 3.10 environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Prepare a `.env` file in the project root and define the required environment variables described below.

## Running the pipeline

Execute the entrypoint script:

```bash
python run_pipeline.py
```

This script sequentially executes the helper scripts located in the `scripts/` directory.

## Enabling the GitHub workflow

The workflow file is stored at `.github/workflows/daily-pipeline.yml.txt`.  Rename this file to `daily-pipeline.yml` on the default branch to activate the scheduled run on GitHub Actions.

## Scripts and environment variables

| Script | Purpose | Key environment variables |
|-------|---------|--------------------------|
| `keyword_auto_pipeline.py` | Collect trending keywords from Google Trends and Twitter and store the filtered result. | `TOPIC_CHANNELS_PATH` (path to topic config), `KEYWORD_OUTPUT_PATH` (output JSON file) |
| `hook_generator.py` | Use OpenAI to generate hook sentences and other content for each keyword. | `OPENAI_API_KEY`, `KEYWORD_OUTPUT_PATH`, `HOOK_OUTPUT_PATH`, `FAILED_HOOK_PATH`, `API_DELAY` |
| `notion_hook_uploader.py` | Upload generated hooks to a Notion database. | `NOTION_API_TOKEN`, `NOTION_HOOK_DB_ID`, `HOOK_OUTPUT_PATH`, `UPLOAD_DELAY` |
| `retry_failed_uploads.py` | Retry uploading hooks that previously failed. | `NOTION_API_TOKEN`, `NOTION_HOOK_DB_ID`, `REPARSED_OUTPUT_PATH`, `RETRY_DELAY` |
| `retry_dashboard_notifier.py` | Send KPI statistics for retry attempts to another Notion database. | `NOTION_API_TOKEN`, `NOTION_KPI_DB_ID`, `REPARSED_OUTPUT_PATH` |
| `scripts/notion_uploader.py` | Upload raw keyword metrics to a Notion database. | `NOTION_API_TOKEN`, `NOTION_DB_ID`, `KEYWORD_OUTPUT_PATH`, `UPLOADED_CACHE_PATH`, `FAILED_UPLOADS_PATH`, `UPLOAD_DELAY` |
| `scripts/retry_failed_uploads.py` | Retry the uploads recorded in `FAILED_HOOK_PATH`. | `NOTION_API_TOKEN`, `NOTION_HOOK_DB_ID`, `FAILED_HOOK_PATH`, `RETRY_DELAY` |
| `run_pipeline.py` | Orchestrate the pipeline by executing the scripts in order. | *(none)* |

All environment variables can be supplied via a `.env` file or directly in your shell environment before running the scripts.

