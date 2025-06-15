# Auto Pipeline

This repository contains a small automation pipeline that collects trending keywords, generates marketing hooks, and publishes them to Notion.

## Pipeline overview

1. **Keyword collection** – `keyword_auto_pipeline.py` scrapes Google Trends and Twitter for trending keywords and writes filtered results to `KEYWORD_OUTPUT_PATH`.
2. **Hook generation** – `hook_generator.py` reads the collected keywords, asks OpenAI for marketing hooks and writes them to `HOOK_OUTPUT_PATH`.
3. **Upload to Notion** – `notion_hook_uploader.py` uploads the generated hooks to your Notion database.
4. **Retry logic** – `retry_failed_uploads.py` and `retry_dashboard_notifier.py` handle re-uploading failed items and pushing KPI summaries.

## Required environment variables

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | API key for OpenAI used by `hook_generator.py`. |
| `NOTION_API_TOKEN` | Access token for the Notion API. |
| `NOTION_HOOK_DB_ID` | Notion database ID used to upload hooks. |
| `NOTION_KPI_DB_ID` | Notion database ID for retry KPI data. |
| `KEYWORD_OUTPUT_PATH` | Path for keyword JSON output (default `data/keyword_output_with_cpc.json`). |
| `HOOK_OUTPUT_PATH` | Path for generated hook JSON (default `data/generated_hooks.json`). |
| `REPARSED_OUTPUT_PATH` | Path for reprocessed/failed items JSON used by the retry steps. |
| `TOPIC_CHANNELS_PATH` | Optional path to topic configuration JSON. |
| `FAILED_HOOK_PATH` | File where failed hook generations are stored. |
| `API_DELAY` | Delay between OpenAI API calls in seconds. |
| `UPLOAD_DELAY` | Delay between Notion uploads in seconds. |
| `RETRY_DELAY` | Delay between retry attempts in seconds. |

## Running locally

Install the required Python packages, set the environment variables above (for example in a `.env` file) and run each stage in order:

```bash
python keyword_auto_pipeline.py
python hook_generator.py
python notion_hook_uploader.py
python retry_failed_uploads.py  # optional – only if there were failures
python retry_dashboard_notifier.py
```

## GitHub Actions

The workflow `.github/workflows/daily-pipeline.yml.txt` runs the pipeline on a schedule. It checks out the repository, installs dependencies and executes `scripts/run_pipeline.py`. The schedule is set to run daily at midnight UTC (09:00 KST). You can also trigger it manually via the "workflow_dispatch" action on GitHub.

