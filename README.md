# Auto Pipeline

This repository contains scripts that collect trending keywords, generate marketing hooks using GPT, and upload everything to Notion. The process is automated daily with GitHub Actions and stores intermediate files in the `data/` and `logs/` directories.

## Pipeline Overview
1. **Keyword collection**: `keyword_auto_pipeline.py` gathers trending terms from Google Trends and Twitter.
2. **GPT hook generation**: `hook_generator.py` uses the keywords to generate short-form hooks, blog draft paragraphs and video titles.
3. **Notion upload**: `notion_hook_uploader.py` (and related scripts) create pages in a Notion database.
4. **Retry + KPI dashboard**: `retry_failed_uploads.py` retries failed uploads and `retry_dashboard_notifier.py` sends a summary KPI to Notion.

`run_pipeline.py` orchestrates these steps in sequence.

## Required Environment Variables

Set the following variables before running the scripts:

- `OPENAI_API_KEY` – API key for OpenAI.
- `NOTION_API_TOKEN` – token for the Notion API.
- `NOTION_HOOK_DB_ID` – Notion database ID for generated hooks.
- `NOTION_KPI_DB_ID` – Notion database ID for KPI logging.
- `NOTION_DB_ID` – Notion database ID for keyword upload.
- `TOPIC_CHANNELS_PATH` – path to the topic configuration JSON file.
- `KEYWORD_OUTPUT_PATH` – output JSON file for collected keywords.
- `HOOK_OUTPUT_PATH` – file containing generated hooks.
- `FAILED_HOOK_PATH` – file to store failed GPT generations.
- `REPARSED_OUTPUT_PATH` – file used when retrying uploads.
- `UPLOAD_DELAY` – delay between Notion uploads.
- `RETRY_DELAY` – delay between retry attempts.
- `API_DELAY` – delay between GPT API calls.
- `UPLOADED_CACHE_PATH` – path to the uploaded keyword cache file.
- `FAILED_UPLOADS_PATH` – path to store failed Notion uploads.

## Usage

Install dependencies and run the full pipeline:

```bash
pip install -r requirements.txt
python run_pipeline.py
```

Generated JSON files are stored under the `data/` directory while logs are saved under `logs/`.

## GitHub Actions

The repository includes a workflow (`.github/workflows/daily-pipeline.yml.txt`) that triggers the pipeline every day. Workflow logs and the file `logs/failed_keywords_reparsed.json` are uploaded as workflow artifacts.
