# Auto Pipeline

This repository contains scripts for generating marketing hooks, uploading them to Notion, and tracking KPI dashboards. The pipeline can be run locally or via the included GitHub Actions workflow.

## Environment Variables
The following variables are read from `.env` or the environment:

- `OPENAI_API_KEY` – API key for OpenAI (used by `hook_generator.py`).
- `NOTION_API_TOKEN` – Notion integration token required for all Notion operations.
- `NOTION_HOOK_DB_ID` – Database ID for generated hooks.
- `NOTION_KPI_DB_ID` – Database ID for KPI statistics.
- `NOTION_DB_ID` – Database ID used by `notion_uploader.py`.
- `KEYWORD_OUTPUT_PATH` – Path to store generated keyword data. Default: `data/keyword_output_with_cpc.json`.
- `HOOK_OUTPUT_PATH` – Path for generated hook content. Default: `data/generated_hooks.json`.
- `FAILED_HOOK_PATH` – File where failed hook generations are written. Default: `logs/failed_hooks.json`.
- `UPLOAD_DELAY` – Delay between Notion API calls in seconds.
- `RETRY_DELAY` – Delay when retrying failed uploads.
- `UPLOADED_CACHE_PATH` – Cache file for uploaded keywords.
- `FAILED_UPLOADS_PATH` – File to record keywords that failed to upload.
- `REPARSED_OUTPUT_PATH` – File containing reparsed failed keywords for retries.
- `SLACK_WEBHOOK_URL` – Optional webhook for notifications from GitHub Actions.
- `TOPIC_CHANNELS_PATH` – Path to JSON topic configuration (default `config/topic_channels.json`).

## Installation
1. Install Python 3.10 or later.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in the required values.

## Running the Pipeline
Execute all stages using:

```bash
python scripts/run_pipeline.py
```

Individual stages can be run by calling the corresponding scripts directly (e.g. `python hook_generator.py`).

## GitHub Actions
The workflow in `.github/workflows/daily-pipeline.yml.txt` runs the pipeline every day at midnight (UTC) and on manual dispatch. Secrets must be configured in the repository to supply the environment variables above. Failed keywords are uploaded as an artifact and summarized in the workflow run summary.

## Testing
Unit tests are not included in this repository. Add tests under a `tests` directory and execute with `pytest` when available.

## Example `.env`
```env
OPENAI_API_KEY=your-openai-api-key
NOTION_API_TOKEN=your-notion-token
NOTION_HOOK_DB_ID=your-hook-database-id
NOTION_KPI_DB_ID=your-kpi-database-id
NOTION_DB_ID=your-keyword-database-id
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
```
