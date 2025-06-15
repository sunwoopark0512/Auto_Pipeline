# Auto Pipeline

This repository contains an automated pipeline for gathering trending keywords and uploading generated marketing hooks to Notion.

## Pipeline Overview
1. **Keyword collection** – `keyword_auto_pipeline.py` collects potential keywords from Google Trends and Twitter then saves them to `KEYWORD_OUTPUT_PATH`.
2. **Hook generation** – `hook_generator.py` uses the OpenAI API to create hooks for each keyword and stores results in `HOOK_OUTPUT_PATH`. Failed generations are saved to `FAILED_HOOK_PATH`.
3. **Notion upload** – `notion_hook_uploader.py` uploads generated hooks to a Notion database (`NOTION_HOOK_DB_ID`).
4. **Retry & KPI dashboard** – `retry_failed_uploads.py` and `retry_dashboard_notifier.py` retry failed uploads and push KPI statistics to another Notion database (`NOTION_KPI_DB_ID`).

## Environment Variables
Set the following variables (typically in a `.env` file):
- `OPENAI_API_KEY`
- `NOTION_API_TOKEN`
- `NOTION_HOOK_DB_ID`
- `NOTION_KPI_DB_ID`
- `NOTION_DB_ID`
- `TOPIC_CHANNELS_PATH`
- `KEYWORD_OUTPUT_PATH`
- `HOOK_OUTPUT_PATH`
- `FAILED_HOOK_PATH`
- `REPARSED_OUTPUT_PATH`
- `UPLOAD_DELAY`
- `RETRY_DELAY`
- `API_DELAY`
- `UPLOADED_CACHE_PATH`
- `FAILED_UPLOADS_PATH`

## Installation
Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Running the Pipeline
Run the complete pipeline locally with:
```bash
python run_pipeline.py
```

## Scheduled Workflow
A GitHub Actions workflow runs `scripts/run_pipeline.py` every day at 00:00 UTC and uploads logs such as `logs/failed_keywords_reparsed.json`. See `.github/workflows/daily-pipeline.yml.txt` for details.
