# Auto Pipeline

This repository contains a set of scripts for collecting trending keywords and automatically uploading marketing hooks to Notion. The pipeline fetches keyword data, generates short form hooks using OpenAI, and records the results in Notion databases. A GitHub Actions workflow executes the pipeline on a schedule.

## Required Environment Variables
Create a `.env` file or export the following variables before running any script:

- `OPENAI_API_KEY` – API key used by `hook_generator.py` for GPT requests.
- `NOTION_API_TOKEN` – Token for accessing the Notion API.
- `NOTION_HOOK_DB_ID` – Database ID where generated hooks are stored.
- `NOTION_DB_ID` – Database ID for the raw keyword table (used by `scripts/notion_uploader.py`).
- `NOTION_KPI_DB_ID` – Database for KPI logging when running `retry_dashboard_notifier.py`.
- Optional paths such as `KEYWORD_OUTPUT_PATH`, `HOOK_OUTPUT_PATH` or `REPARSED_OUTPUT_PATH` may be customised if the defaults are unsuitable.

## Installing Dependencies
Install Python packages using the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Running the Pipeline Locally
1. Ensure all required environment variables are configured.
2. Collect trending keywords:
   ```bash
   python keyword_auto_pipeline.py
   ```
3. Generate hook sentences with GPT:
   ```bash
   python hook_generator.py
   ```
4. Upload generated hooks to Notion:
   ```bash
   python notion_hook_uploader.py
   ```
5. To execute the retry and notification steps together, run the orchestrator:
   ```bash
   python run_pipeline.py
   ```

## GitHub Actions Workflow
The file `.github/workflows/daily-pipeline.yml.txt` defines a scheduled workflow. It runs every day via cron and can also be triggered manually. The workflow performs the following actions:

1. Checks out the repository.
2. Sets up Python `3.10`.
3. Installs dependencies using `requirements.txt`.
4. Executes the pipeline entrypoint (`python scripts/run_pipeline.py`).
5. Uploads a JSON artifact containing failed keywords if any remain.
6. Appends a short summary to the workflow run.

Secrets configured in the GitHub repository provide the required environment variables for the workflow.
