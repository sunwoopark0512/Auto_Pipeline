# Auto Pipeline

This repository contains scripts that collect trending keywords, generate marketing hooks using GPT, and upload them to Notion.

## Required Environment Variables

Set the following variables (e.g., in a `.env` file or your shell):

- `OPENAI_API_KEY` – API key used by `hook_generator.py` for GPT access.
- `NOTION_API_TOKEN` – token for all Notion API calls.
- `NOTION_HOOK_DB_ID` – database ID where hooks are stored.
- `NOTION_KPI_DB_ID` – database ID where retry KPI metrics are logged.
- `NOTION_DB_ID` – database ID for uploading raw keywords via `scripts/notion_uploader.py`.
- `KEYWORD_OUTPUT_PATH` – output path for collected keyword data (default `data/keyword_output_with_cpc.json`).
- `HOOK_OUTPUT_PATH` – location for generated hooks (default `data/generated_hooks.json`).
- `FAILED_HOOK_PATH` – failed hook output path used by retry scripts (default `logs/failed_hooks.json`).
- `REPARSED_OUTPUT_PATH` – path to the parsed or retried data used for KPI notifications (default `logs/failed_keywords_reparsed.json`).
- `UPLOAD_DELAY`, `RETRY_DELAY`, `API_DELAY` – optional delays between API calls.
- `UPLOADED_CACHE_PATH` and `FAILED_UPLOADS_PATH` – caches used by `scripts/notion_uploader.py`.
- `TOPIC_CHANNELS_PATH` – path to the topic configuration JSON (default `config/topic_channels.json`).

## Script Overview

- **`keyword_auto_pipeline.py`** – Collects trending keywords from Google Trends and Twitter and writes the filtered list to `KEYWORD_OUTPUT_PATH`.
- **`hook_generator.py`** – Uses GPT (via `OPENAI_API_KEY`) to create marketing hooks for each keyword found by the previous step. Results are saved to `HOOK_OUTPUT_PATH`.
- **`notion_hook_uploader.py`** – Uploads the generated hooks to the Notion database specified by `NOTION_HOOK_DB_ID`.
- **`retry_failed_uploads.py`** – Reattempts any failed Notion uploads stored in `REPARSED_OUTPUT_PATH`.
- **`retry_dashboard_notifier.py`** – Sends a summary of retry results to the KPI database referenced by `NOTION_KPI_DB_ID`.
- **`scripts/notion_uploader.py`** – Alternate uploader for raw keyword data to a Notion database (`NOTION_DB_ID`).
- **`scripts/retry_failed_uploads.py`** – Retry logic for failed hook uploads saved to `FAILED_HOOK_PATH`.
- **`run_pipeline.py`** – Convenience script that runs several of the above components in sequence.

### Typical Execution Order

1. `keyword_auto_pipeline.py`
2. `hook_generator.py`
3. `notion_hook_uploader.py`
4. `retry_failed_uploads.py`
5. `retry_dashboard_notifier.py`

`run_pipeline.py` can be used to automate these steps.

## Running the GitHub Workflow Manually

The workflow definition lives in `.github/workflows/daily-pipeline.yml.txt`. After renaming it to `daily-pipeline.yml` and committing the change, navigate to the **Actions** tab in GitHub. Select **"Daily Notion Hook Pipeline"** and use the **Run workflow** button to trigger the job manually. The workflow requires the environment secrets listed above to be configured in the repository settings.
