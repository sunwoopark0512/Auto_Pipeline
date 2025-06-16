# Auto Pipeline

This repository contains a collection of scripts used to generate marketing hooks from trending keywords and upload them to Notion. The automation can be run locally or through the provided GitHub Actions workflow.

## Scripts

| Script | Purpose | Required Environment Variables |
|-------|---------|--------------------------------|
|`keyword_auto_pipeline.py`|Collect trending keywords from Google Trends and Twitter. Saves results to `data/keyword_output_with_cpc.json`.|`TOPIC_CHANNELS_PATH` (path to `config/topic_channels.json`), `KEYWORD_OUTPUT_PATH`|
|`hook_generator.py`|Generate hooks for each keyword using the OpenAI API.|`OPENAI_API_KEY`, `KEYWORD_OUTPUT_PATH`, `HOOK_OUTPUT_PATH`, `FAILED_HOOK_PATH`, `API_DELAY`|
|`notion_hook_uploader.py`|Upload generated hooks to a Notion database.|`NOTION_API_TOKEN`, `NOTION_HOOK_DB_ID`, `HOOK_OUTPUT_PATH`, `UPLOAD_DELAY`|
|`retry_failed_uploads.py`|Retry uploading failed hooks stored in `logs/failed_keywords_reparsed.json`.|`NOTION_API_TOKEN`, `NOTION_HOOK_DB_ID`, `REPARSED_OUTPUT_PATH`, `RETRY_DELAY`|
|`retry_dashboard_notifier.py`|Send KPI summary of retry attempts to a Notion dashboard.|`NOTION_API_TOKEN`, `NOTION_KPI_DB_ID`, `REPARSED_OUTPUT_PATH`|
|`scripts/notion_uploader.py`|Upload filtered keywords to a Notion database.|`NOTION_API_TOKEN`, `NOTION_DB_ID`, `KEYWORD_OUTPUT_PATH`, `UPLOAD_DELAY`, `UPLOADED_CACHE_PATH`, `FAILED_UPLOADS_PATH`|
|`scripts/retry_failed_uploads.py`|Retry uploading keywords that failed to upload from `logs/failed_keywords.json`.|`NOTION_API_TOKEN`, `NOTION_HOOK_DB_ID`, `FAILED_HOOK_PATH`, `RETRY_DELAY`|
|`run_pipeline.py`|Execute the main pipeline which runs several scripts in sequence.|None|

## Installation

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Running the Pipeline

After setting the required environment variables (e.g. in a `.env` file), run:

```bash
python run_pipeline.py
```

The script will sequentially execute the pipeline steps defined in `run_pipeline.py`.

## GitHub Actions Workflow

The workflow file `.github/workflows/daily-pipeline.yml` installs dependencies and executes the pipeline on a daily schedule. Commit this file to GitHub to activate the workflow or trigger it manually from the Actions tab.

