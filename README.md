# Auto Pipeline

This repository contains scripts for generating marketing hooks from trending keywords and uploading the results to Notion.

## Environment Variables
Create a `.env` file in the project root (or set these values in your environment) before running any scripts:

- `OPENAI_API_KEY` – API key for OpenAI GPT calls.
- `NOTION_API_TOKEN` – Notion integration token with access to your databases.
- `NOTION_DB_ID` – Notion database ID for keyword metrics (used in `scripts/notion_uploader.py`).
- `NOTION_HOOK_DB_ID` – Notion database ID where generated hooks will be stored.
- `NOTION_KPI_DB_ID` – Database for storing retry KPI statistics.
- `KEYWORD_OUTPUT_PATH` – Path to save keyword results. Default: `data/keyword_output_with_cpc.json`.
- `HOOK_OUTPUT_PATH` – Path for generated hook data. Default: `data/generated_hooks.json`.
- `FAILED_HOOK_PATH` – Location to store hooks that failed to generate. Default: `logs/failed_hooks.json`.
- `UPLOADED_CACHE_PATH` – Cache file of uploaded keywords. Default: `data/uploaded_keywords_cache.json`.
- `FAILED_UPLOADS_PATH` – File for failed Notion uploads. Default: `logs/failed_uploads.json`.
- `REPARSED_OUTPUT_PATH` – File used when retrying failed uploads. Default: `logs/failed_keywords_reparsed.json`.
- `UPLOAD_DELAY` – Delay between Notion uploads in seconds (float).
- `RETRY_DELAY` – Delay between retry attempts in seconds (float).
- `API_DELAY` – Delay between OpenAI API calls in seconds (float).

## Running the Pipeline Locally
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Ensure your `.env` file is populated with the variables above.
3. Execute the pipeline:
   ```bash
   python run_pipeline.py
   ```
   The entrypoint script sequentially calls the individual scripts defined in `run_pipeline.py`.

Each module can also be run independently if you need to debug specific stages (e.g. `python keyword_auto_pipeline.py`).

## GitHub Workflow
A GitHub Actions workflow is defined in `.github/workflows/daily-pipeline.yml.txt`. It runs every day via cron and can also be triggered manually. The workflow:

1. Checks out the repository and installs Python 3.10.
2. Installs requirements from `requirements.txt`.
3. Runs the pipeline with `python scripts/run_pipeline.py` using secret environment variables (`OPENAI_API_KEY`, `NOTION_API_TOKEN`, etc.).
4. Uploads any failed keyword JSON as an artifact and appends a summary to the workflow run.

This automation allows the Notion hook generation pipeline to run on a schedule without manual intervention.
