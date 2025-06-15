# Auto Pipeline

This repository contains scripts for an automated pipeline that collects trending keywords, generates marketing hooks with GPT, uploads them to Notion, and reports retry statistics.

## Pipeline Overview

1. **Keyword collection** – `keyword_auto_pipeline.py` gathers popular topics from multiple sources (Google Trends, Twitter) and saves them to JSON.
2. **Hook generation** – `hook_generator.py` reads the keywords and uses OpenAI GPT to create short-form hooks and content ideas.
3. **Uploading to Notion** – `notion_hook_uploader.py` pushes the generated hooks to a Notion database.
4. **Retry & dashboard** – failed uploads are retried with `retry_failed_uploads.py`, and `retry_dashboard_notifier.py` records retry KPIs to another Notion database.

The entry point `run_pipeline.py` orchestrates these steps sequentially.

## Environment Variables

The scripts rely on a set of environment variables. Provide them via a `.env` file or through the environment:

- `OPENAI_API_KEY` – API key for GPT calls.
- `NOTION_API_TOKEN` – token for Notion API access.
- `NOTION_HOOK_DB_ID` – target Notion database for hooks.
- `NOTION_KPI_DB_ID` – database for retry statistics.
- `NOTION_DB_ID` – database used by `scripts/notion_uploader.py`.
- `TOPIC_CHANNELS_PATH` – path to topic configuration JSON.
- `KEYWORD_OUTPUT_PATH` – location for collected keywords JSON.
- `HOOK_OUTPUT_PATH` – output file for generated hooks.
- `FAILED_HOOK_PATH` – file where failed GPT generations are stored.
- `REPARSED_OUTPUT_PATH` – path used when retrying failed uploads.
- `FAILED_UPLOADS_PATH` – failed Notion upload list.
- `UPLOADED_CACHE_PATH` – cache file to avoid duplicate uploads.
- `UPLOAD_DELAY` – delay (seconds) between Notion uploads.
- `RETRY_DELAY` – delay when retrying failed uploads.
- `API_DELAY` – wait time between GPT API calls.

## Installation & Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the entire pipeline:
   ```bash
   python run_pipeline.py
   ```

Generated files are stored under `data/` and logs under `logs/`.

## GitHub Actions

The workflow `.github/workflows/daily-pipeline.yml.txt` executes the pipeline every day via GitHub Actions. It installs dependencies, runs `python scripts/run_pipeline.py`, and uploads `logs/failed_keywords_reparsed.json` as an artifact. Workflow summaries also include basic execution information.

Output JSON files and logs can be found in the `data/` and `logs/` directories of the repository.

