# Auto Pipeline

This repository automates collecting trending keywords, generating marketing hooks with OpenAI, and uploading the results to Notion. It can run locally or through the included GitHub Actions workflow.

## Pipeline Overview
1. **`keyword_auto_pipeline.py`** – Collects trending keywords from Google Trends and Twitter and saves a filtered list to `KEYWORD_OUTPUT_PATH`.
2. **`hook_generator.py`** – Uses the keywords to generate hook sentences, blog drafts, and YouTube titles with the OpenAI API. Results are written to `HOOK_OUTPUT_PATH` and failures to `FAILED_HOOK_PATH`.
3. **`notion_hook_uploader.py`** – Uploads generated hooks to the Notion database defined by `NOTION_HOOK_DB_ID`.
4. **`retry_failed_uploads.py`** – Attempts to re‑upload failed items from `REPARSED_OUTPUT_PATH`.
5. **`retry_dashboard_notifier.py`** – Summarizes retry results and pushes KPI metrics to another Notion database.

Additional helper scripts live in the `scripts/` directory for uploading raw keywords and retrying failed uploads.

## Required Environment Variables
Environment variables are loaded from a `.env` file. See `.env.example` for the full list. The most important variables are:

- `OPENAI_API_KEY` – API key for OpenAI.
- `NOTION_API_TOKEN` – Token for accessing the Notion API.
- `NOTION_DB_ID` – Notion database for keyword uploads.
- `NOTION_HOOK_DB_ID` – Notion database for hook uploads.
- `NOTION_KPI_DB_ID` – Notion database for retry KPI tracking.
- `SLACK_WEBHOOK_URL` – Optional webhook used by GitHub Actions.

Paths such as `KEYWORD_OUTPUT_PATH` and `HOOK_OUTPUT_PATH` can also be overridden in the `.env` file.

## Running Locally
1. Install Python 3.10 and required packages (see your environment).
2. Copy `.env.example` to `.env` and fill in the values.
3. Run the pipeline entrypoint:

```bash
python run_pipeline.py
```

Individual scripts can also be executed directly if needed.

## Running with GitHub Actions
The workflow file `.github/workflows/daily-pipeline.yml.txt` runs the pipeline every day via GitHub Actions. Secrets corresponding to the environment variables above must be added to the repository settings. The workflow installs dependencies, executes `python scripts/run_pipeline.py`, and uploads any failed keywords as artifacts.

