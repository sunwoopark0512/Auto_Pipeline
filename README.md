# Auto Pipeline

This repository contains a set of scripts for generating marketing hooks from trending keywords and uploading them to Notion. The pipeline also retries failed uploads and records KPI metrics.

## Pipeline Overview
1. **Keyword Collection** – `keyword_auto_pipeline.py` gathers trending keywords from Google Trends and Twitter and saves them to a JSON file.
2. **Hook Generation** – `hook_generator.py` uses OpenAI to generate hook sentences, blog drafts and video titles for each keyword.
3. **Upload to Notion** – `notion_hook_uploader.py` uploads the generated content to a Notion database.
4. **Retry and KPI Update** – `retry_failed_uploads.py` and `retry_dashboard_notifier.py` handle re‑uploads of failed items and push success metrics to another Notion dashboard.
5. **Orchestration** – `run_pipeline.py` sequentially executes the above scripts.

Output JSON files are written under the `data/` directory and logs are stored under `logs/` (both created automatically if they do not exist).

## Required Environment Variables
Each script reads its configuration from environment variables (typically loaded from a `.env` file):

| Script | Variables |
|-------|-----------|
|`keyword_auto_pipeline.py`|`TOPIC_CHANNELS_PATH` (path to topic_channels.json), `KEYWORD_OUTPUT_PATH` (output JSON path)|
|`hook_generator.py`|`KEYWORD_OUTPUT_PATH` (input from previous step), `HOOK_OUTPUT_PATH` (generated hooks JSON), `FAILED_HOOK_PATH` (failed hooks JSON), `OPENAI_API_KEY`, `API_DELAY`|
|`notion_hook_uploader.py`|`NOTION_API_TOKEN`, `NOTION_HOOK_DB_ID`, `HOOK_OUTPUT_PATH` (input), `UPLOAD_DELAY`|
|`retry_failed_uploads.py`|`NOTION_API_TOKEN`, `NOTION_HOOK_DB_ID`, `REPARSED_OUTPUT_PATH` (failed keywords file), `RETRY_DELAY`|
|`retry_dashboard_notifier.py`|`NOTION_API_TOKEN`, `NOTION_KPI_DB_ID`, `REPARSED_OUTPUT_PATH`|
|`scripts/notion_uploader.py`|`NOTION_API_TOKEN`, `NOTION_DB_ID`, `KEYWORD_OUTPUT_PATH`, `UPLOAD_DELAY`, `UPLOADED_CACHE_PATH`, `FAILED_UPLOADS_PATH`|
|`scripts/retry_failed_uploads.py`|`NOTION_API_TOKEN`, `NOTION_HOOK_DB_ID`, `FAILED_HOOK_PATH`, `RETRY_DELAY`|

## Running Individual Scripts
Execute each script with Python after setting the required environment variables:

```bash
python keyword_auto_pipeline.py        # Collect trending keywords
python hook_generator.py               # Generate hook text using OpenAI
python notion_hook_uploader.py         # Upload generated hooks to Notion
python retry_failed_uploads.py         # Retry uploads that previously failed
python retry_dashboard_notifier.py     # Push retry KPI metrics to Notion
```

To run the full sequence automatically, execute:

```bash
python run_pipeline.py
```

The pipeline expects all outputs to be located in `data/` with error logs in `logs/`. Check these folders for files such as `keyword_output_with_cpc.json`, `generated_hooks.json`, and `upload_failed_hooks.json` after running each step.
