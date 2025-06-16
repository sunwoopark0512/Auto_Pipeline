# Auto Pipeline

This project automates trending keyword collection, hook generation through GPT, and uploading results to Notion. A GitHub Actions workflow can run the entire pipeline on a schedule.

## Installation

1. Create a Python 3.10 environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Environment variables

Each script reads values from environment variables (typically loaded from a `.env` file).

| Script | Required variables | Optional variables |
|-------|-------------------|-------------------|
| `hook_generator.py` | `OPENAI_API_KEY` | `KEYWORD_OUTPUT_PATH` (default `data/keyword_output_with_cpc.json`), `HOOK_OUTPUT_PATH` (default `data/generated_hooks.json`), `FAILED_HOOK_PATH` (default `logs/failed_hooks.json`), `API_DELAY` (default `1.0`)
| `notion_hook_uploader.py` | `NOTION_API_TOKEN`, `NOTION_HOOK_DB_ID` | `HOOK_OUTPUT_PATH` (default `data/generated_hooks.json`), `UPLOAD_DELAY` (default `0.5`)
| `keyword_auto_pipeline.py` | – | `TOPIC_CHANNELS_PATH` (default `config/topic_channels.json`), `KEYWORD_OUTPUT_PATH` (default `data/keyword_output_with_cpc.json`)
| `retry_failed_uploads.py` | `NOTION_API_TOKEN`, `NOTION_HOOK_DB_ID` | `REPARSED_OUTPUT_PATH` (default `logs/failed_keywords_reparsed.json`), `RETRY_DELAY` (default `0.5`)
| `retry_dashboard_notifier.py` | `NOTION_API_TOKEN`, `NOTION_KPI_DB_ID` | `REPARSED_OUTPUT_PATH` (default `logs/failed_keywords_reparsed.json`)
| `scripts/notion_uploader.py` | `NOTION_API_TOKEN`, `NOTION_DB_ID` | `KEYWORD_OUTPUT_PATH` (default `data/keyword_output_with_cpc.json`), `UPLOAD_DELAY` (default `0.5`), `UPLOADED_CACHE_PATH` (default `data/uploaded_keywords_cache.json`), `FAILED_UPLOADS_PATH` (default `logs/failed_uploads.json`)
| `scripts/retry_failed_uploads.py` | `NOTION_API_TOKEN`, `NOTION_HOOK_DB_ID` | `FAILED_HOOK_PATH` (default `logs/failed_keywords.json`), `RETRY_DELAY` (default `0.5`)

## Running the pipeline

Run all steps with:
```bash
python run_pipeline.py
```
Scripts listed in `run_pipeline.py` will execute sequentially. You can also run individual scripts directly using `python <script_name>.py`.

## GitHub workflow

The repository includes `.github/workflows/daily-pipeline.yml.txt` which schedules the pipeline daily and allows manual dispatch. Store secrets (`OPENAI_API_KEY`, `NOTION_API_TOKEN`, `NOTION_HOOK_DB_ID`, `NOTION_KPI_DB_ID`, and `SLACK_WEBHOOK_URL`) in your repository settings. The workflow checks out the code, installs dependencies with `pip install -r requirements.txt`, then runs `python scripts/run_pipeline.py`.

