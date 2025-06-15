# Auto Pipeline

This repository contains a set of scripts that collect trending keywords, generate marketing hooks using GPT, and upload the results to Notion.  Failed items are retried automatically and summary metrics are uploaded to a Notion dashboard.

## Components

1. **Keyword collection** (`keyword_auto_pipeline.py`)
   - Builds keyword pairs from `config/topic_channels.json`.
   - Gathers metrics from Google Trends and Twitter.
   - Writes filtered results to `data/keyword_output_with_cpc.json`.
2. **GPT hook generation** (`hook_generator.py`)
   - Uses OpenAI's API to create hook lines, blog paragraphs and video titles.
   - Stores output in `data/generated_hooks.json` and logs failures in `logs/failed_hooks.json`.
3. **Notion upload** (`notion_hook_uploader.py` and `scripts/notion_uploader.py`)
   - Uploads generated hooks or keywords to the specified Notion database.
   - Keeps a cache and records failed uploads for later retry.
4. **Retries and KPI reporting** (`retry_failed_uploads.py`, `retry_dashboard_notifier.py`)
   - Attempts to upload any previously failed items and pushes KPI statistics to Notion.
5. **Pipeline runner** (`run_pipeline.py`)
   - Executes the above steps in order.

Output files are written under the `data/` and `logs/` directories.

## Environment variables

Create a `.env` file based on `.env.example` and populate it with your credentials.  Important variables include:

- `OPENAI_API_KEY` – API key for GPT requests.
- `NOTION_API_TOKEN` – Notion integration token.
- `NOTION_DB_ID` – ID of the keyword database.
- `NOTION_HOOK_DB_ID` – ID of the hook content database.
- `NOTION_KPI_DB_ID` – ID of the KPI dashboard.
- Paths such as `KEYWORD_OUTPUT_PATH`, `HOOK_OUTPUT_PATH`, and `REPARSED_OUTPUT_PATH`.

See `.env.example` for the full list.

## Installation

Install the required Python packages and run the pipeline:

```bash
pip install -r requirements.txt
python run_pipeline.py
```

## GitHub Actions

A workflow defined in `.github/workflows/daily-pipeline.yml.txt` runs the pipeline every day.  It installs dependencies, executes the pipeline, and uploads any failure logs as artifacts.

The main outputs are JSON files under `data/` and `logs/`, which can be inspected or uploaded to Notion depending on the step.
