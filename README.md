# Notion Hook Pipeline

This repository contains automation scripts to generate engaging hooks from trending keywords and send them to a Notion database. It combines OpenAI for text generation and the Notion API for storage. The pipeline can run locally or on GitHub Actions.

## Environment variables
Set the following variables in a `.env` file or your shell before running the pipeline:

- `OPENAI_API_KEY` – API key for OpenAI completions.
- `NOTION_API_TOKEN` – token for the Notion integration.
- `NOTION_HOOK_DB_ID` – ID of the Notion database used to store generated hooks.
- `NOTION_KPI_DB_ID` – ID of the database for KPI logging (optional).
- `KEYWORD_OUTPUT_PATH` – path to the keyword JSON produced by `keyword_auto_pipeline.py`.
- `HOOK_OUTPUT_PATH` – where `hook_generator.py` writes generated hooks.
- `FAILED_HOOK_PATH` – file path for failed OpenAI generations.
- `REPARSED_OUTPUT_PATH` – file used when retrying failed uploads.
- `UPLOAD_DELAY` – delay in seconds between Notion API requests.
- `RETRY_DELAY` – delay in seconds between retry attempts.
- `API_DELAY` – delay between OpenAI API calls.

## Running locally
1. Install Python 3.10 and clone this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with the variables listed above.
4. Run the pipeline:
   ```bash
   python run_pipeline.py
   ```
   The script will execute each step in order – generating hooks and uploading them to Notion.

## Running with GitHub Actions
The workflow file `.github/workflows/daily-pipeline.yml.txt` runs the pipeline on a schedule and can also be triggered manually.

1. Add the required environment variables as repository secrets (`OPENAI_API_KEY`, `NOTION_API_TOKEN`, `NOTION_HOOK_DB_ID`, `NOTION_KPI_DB_ID`, `SLACK_WEBHOOK_URL`).
2. On each run, the action installs dependencies and executes:
   ```bash
   python scripts/run_pipeline.py
   ```
3. Any failed items are uploaded as workflow artifacts and a short summary is appended to the workflow run.

This allows the Notion hook pipeline to run automatically every day or on demand through GitHub.
