# Auto Pipeline

This repository contains a set of scripts for collecting trending keywords, generating marketing hooks using GPT, and uploading the results to Notion. It also includes tools for retrying failed uploads and logging KPI metrics.

## Setup

1. **Python**: The pipeline uses Python 3.10.
2. **Install dependencies**:
   ```bash
   pip install openai notion_client python-dotenv pytrends snscrape
   ```
3. **Environment variables**: Create a `.env` file in the repository root and set the following variables.

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | API key for OpenAI (used by `hook_generator.py`) |
| `NOTION_API_TOKEN` | Token for accessing Notion APIs |
| `NOTION_DB_ID` | Database ID for uploading keywords (used by `scripts/notion_uploader.py`) |
| `NOTION_HOOK_DB_ID` | Database ID for generated hooks |
| `NOTION_KPI_DB_ID` | Database ID for retry KPI logging |
| `TOPIC_CHANNELS_PATH` | Path to topic JSON (default: `config/topic_channels.json`) |
| `KEYWORD_OUTPUT_PATH` | Path for keyword output JSON (default: `data/keyword_output_with_cpc.json`) |
| `HOOK_OUTPUT_PATH` | Path for generated hooks JSON (default: `data/generated_hooks.json`) |
| `FAILED_HOOK_PATH` | Path for failed GPT results (default: `logs/failed_hooks.json`) |
| `REPARSED_OUTPUT_PATH` | Path used for retry logs (default: `logs/failed_keywords_reparsed.json`) |
| `RETRY_DELAY` | Delay between retry attempts (default: `0.5`) |
| `UPLOAD_DELAY` | Delay between Notion uploads (default: `0.5`) |
| `API_DELAY` | Delay between OpenAI API calls (default: `1.0`) |
| `UPLOADED_CACHE_PATH` | Cache file for uploaded keywords |
| `FAILED_UPLOADS_PATH` | File for failed Notion uploads |

Only variables relevant to the scripts you run need to be configured.

## Running the pipeline

To execute all steps locally, run:

```bash
python run_pipeline.py
```

Individual scripts can also be run directly (e.g. `python keyword_auto_pipeline.py`).

## Scheduled execution

A GitHub Actions workflow is provided in `.github/workflows/daily-pipeline.yml.txt`. Rename the file to `daily-pipeline.yml` to enable it in your repository. The workflow runs daily at midnight UTC and executes `python scripts/run_pipeline.py`. It expects the required secrets (`OPENAI_API_KEY`, `NOTION_API_TOKEN`, etc.) to be added to the repository settings.

