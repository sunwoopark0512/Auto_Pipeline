# Auto Pipeline

This repository contains scripts for collecting trending keywords, generating marketing hooks using GPT, and uploading the results to Notion.

## Pipeline Overview

1. **Keyword collection** (`keyword_auto_pipeline.py`)
   - Gathers keywords from Google Trends and Twitter.
   - Filters them based on predefined metrics.
   - Saves the result to `KEYWORD_OUTPUT_PATH`.

2. **Hook generation** (`hook_generator.py`)
   - Reads the keywords JSON file.
   - Uses OpenAI's API to generate hook sentences, blog drafts and video titles.
   - Stores successful results in `HOOK_OUTPUT_PATH` and failures in `FAILED_HOOK_PATH`.

3. **Notion upload** (`notion_hook_uploader.py`)
   - Uploads generated hooks to the Notion database specified by `NOTION_HOOK_DB_ID`.
   - Keeps a log of failed uploads.

4. **Retry scripts**
   - `retry_failed_uploads.py` attempts to upload items that previously failed.
   - `retry_dashboard_notifier.py` summarizes retry results and sends them to a KPI database.

## Environment Variables

| Variable | Description |
| --- | --- |
| `OPENAI_API_KEY` | API key for OpenAI GPT access |
| `NOTION_API_TOKEN` | Notion integration token |
| `NOTION_HOOK_DB_ID` | Notion database ID for generated hooks |
| `NOTION_KPI_DB_ID` | Notion database ID for retry KPI records |
| `NOTION_DB_ID` | Notion database ID used by `notion_uploader.py` |
| `TOPIC_CHANNELS_PATH` | Path to topic configuration JSON |
| `KEYWORD_OUTPUT_PATH` | Output path for collected keywords |
| `HOOK_OUTPUT_PATH` | Output path for generated hooks |
| `FAILED_HOOK_PATH` | Path for storing failed hook generations |
| `REPARSED_OUTPUT_PATH` | File used by retry scripts to store failed items |
| `UPLOADED_CACHE_PATH` | Cache file of successfully uploaded keywords |
| `FAILED_UPLOADS_PATH` | File for failed keyword uploads |
| `API_DELAY` | Delay in seconds between GPT API calls |
| `UPLOAD_DELAY` | Delay in seconds between Notion uploads |
| `RETRY_DELAY` | Delay in seconds between retry attempts |

## Local Execution

Install the dependencies listed in `requirements.txt` and set the required environment variables (for example in a `.env` file). Then run each stage sequentially:

```bash
python keyword_auto_pipeline.py
python hook_generator.py
python notion_hook_uploader.py
python retry_failed_uploads.py  # optional
python retry_dashboard_notifier.py  # optional
```

Alternatively, run `python run_pipeline.py` to execute the scripts defined in `PIPELINE_SEQUENCE`.

## GitHub Actions

The workflow `.github/workflows/daily-pipeline.yml.txt` runs the pipeline daily using scheduled GitHub Actions. Secrets provide the API keys and database IDs. The workflow installs dependencies, runs `scripts/run_pipeline.py`, and uploads any failed items as an artifact.

