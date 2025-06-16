# Auto_Pipeline

## Purpose

This repository provides an automated pipeline for collecting trending keywords, generating marketing hook text with GPT, and uploading the results to Notion dashboards.  The workflow gathers data from Google Trends and Twitter, creates engaging hook phrases, and keeps track of retry statistics.

## Setup

1. **Python**: Ensure Python 3.10+ is installed.
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Environment variables**: Create a `.env` file in the project root and set the variables described below.  Most scripts have sensible defaults so only API keys and database IDs are strictly required.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | API key for the OpenAI GPT models. |
| `NOTION_API_TOKEN` | Token for the Notion API. |
| `NOTION_HOOK_DB_ID` | Database ID used by `notion_hook_uploader.py` and retry scripts. |
| `NOTION_DB_ID` | Database ID for uploading raw keyword data. |
| `NOTION_KPI_DB_ID` | Database ID for saving retry KPI statistics. |
| `TOPIC_CHANNELS_PATH` | (default `config/topic_channels.json`) JSON file listing topics. |
| `KEYWORD_OUTPUT_PATH` | (default `data/keyword_output_with_cpc.json`) output from `keyword_auto_pipeline.py`. |
| `HOOK_OUTPUT_PATH` | (default `data/generated_hooks.json`) generated hooks from `hook_generator.py`. |
| `FAILED_HOOK_PATH` | (default `logs/failed_hooks.json`) failed hook entries. |
| `UPLOADED_CACHE_PATH` | (default `data/uploaded_keywords_cache.json`) cache of uploaded keywords. |
| `FAILED_UPLOADS_PATH` | (default `logs/failed_uploads.json`) failed Notion uploads. |
| `REPARSED_OUTPUT_PATH` | (default `logs/failed_keywords_reparsed.json`) location for parsed retry data. |
| `API_DELAY` | (default `1.0`) delay between OpenAI API requests. |
| `UPLOAD_DELAY` | (default `0.5`) delay between Notion uploads. |
| `RETRY_DELAY` | (default `0.5`) delay between retry attempts. |

## Running `channel_roi_analyzer.py`

A script named `channel_roi_analyzer.py` is expected to analyze ROI metrics for each channel.  After configuring the environment variables above, simply run:

```bash
python channel_roi_analyzer.py
```

Adjust paths or options as required by that script.

## Running the Pipeline

The primary pipeline orchestrator is `run_pipeline.py`.  It sequentially executes the individual scripts located in this repository.

```bash
python run_pipeline.py
```

This command will generate hooks, parse failed results, retry any failed uploads, and post KPI data to Notion.  Review the logs in the `logs/` directory for details of each step.

