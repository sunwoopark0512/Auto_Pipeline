# Auto Pipeline

This repository contains a collection of scripts that generate marketing hooks from trending keywords and uploads them to Notion. A GitHub Actions workflow runs the pipeline daily.

## Requirements
- Python 3.10+
- Access tokens for OpenAI and Notion

Install dependencies:
```bash
pip install -r requirements.txt
```

## Environment variables
Create a `.env` file with the following variables:
- `OPENAI_API_KEY` – API key for OpenAI
- `NOTION_API_TOKEN` – Notion integration token
- `NOTION_HOOK_DB_ID` – Database ID for generated hooks
- `NOTION_KPI_DB_ID` – Database ID for KPI tracking
- `KEYWORD_OUTPUT_PATH` – Path to keyword JSON (default `data/keyword_output_with_cpc.json`)
- `HOOK_OUTPUT_PATH` – Output path for generated hooks (default `data/generated_hooks.json`)
- `FAILED_HOOK_PATH` – Failed hook output path (default `logs/failed_hooks.json`)
- `REPARSED_OUTPUT_PATH` – Failed keyword JSON for retry (default `logs/failed_keywords_reparsed.json`)
- `UPLOAD_DELAY` – Delay between Notion uploads (default `0.5`)
- `RETRY_DELAY` – Delay when retrying failed uploads (default `0.5`)

## Usage
Run the full pipeline locally:
```bash
python run_pipeline.py
```

The daily workflow `.github/workflows/daily-pipeline.yml.txt` executes the pipeline every day at 00:00 UTC.
