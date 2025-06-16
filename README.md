# Auto Pipeline

This project automates the generation of marketing hooks from trending keywords and uploads the results to Notion.  The repository contains several standalone scripts along with a small GitHub Actions workflow to run the pipeline daily.

## Requirements

Install the required Python packages:

```bash
pip install -r requirements.txt
```

A `.env` file (or environment variables) must supply API keys and other settings used by the scripts.

## Scripts Overview

| Script | Purpose | Required Environment Variables |
|-------|---------|--------------------------------|
| `keyword_auto_pipeline.py` | Collects trend and social metrics for topics defined in `config/topic_channels.json` and filters them. Saves the result to `data/keyword_output_with_cpc.json`. | `TOPIC_CHANNELS_PATH` *(optional, defaults to `config/topic_channels.json`)*, `KEYWORD_OUTPUT_PATH` *(optional, defaults to `data/keyword_output_with_cpc.json`)* |
| `hook_generator.py` | Generates hook sentences using OpenAI based on the keyword file from the previous step. Writes results to `data/generated_hooks.json`. | `OPENAI_API_KEY`, `KEYWORD_OUTPUT_PATH`, `HOOK_OUTPUT_PATH`, `FAILED_HOOK_PATH`, `API_DELAY` |
| `notion_hook_uploader.py` | Uploads generated hooks to a Notion database. Failed uploads are stored for retry. | `NOTION_API_TOKEN`, `NOTION_HOOK_DB_ID`, `HOOK_OUTPUT_PATH`, `UPLOAD_DELAY` |
| `retry_failed_uploads.py` | Re‑attempts uploading items that previously failed to upload to Notion. | `NOTION_API_TOKEN`, `NOTION_HOOK_DB_ID`, `REPARSED_OUTPUT_PATH`, `RETRY_DELAY` |
| `retry_dashboard_notifier.py` | Pushes retry KPI statistics to a Notion dashboard database. | `NOTION_API_TOKEN`, `NOTION_KPI_DB_ID`, `REPARSED_OUTPUT_PATH` |
| `run_pipeline.py` | Executes the above scripts in sequence from the `scripts` folder. | – |
| `scripts/notion_uploader.py` | Uploads filtered keyword metrics to a Notion database. | `NOTION_API_TOKEN`, `NOTION_DB_ID`, `KEYWORD_OUTPUT_PATH`, `UPLOAD_DELAY`, `UPLOADED_CACHE_PATH`, `FAILED_UPLOADS_PATH` |
| `scripts/retry_failed_uploads.py` | Older variant for retrying failed hook uploads. | `NOTION_API_TOKEN`, `NOTION_HOOK_DB_ID`, `FAILED_HOOK_PATH`, `RETRY_DELAY` |

## Running Locally

Create a `.env` file with the required variables and then run the pipeline:

```bash
python run_pipeline.py
```

Each step logs information to the console and writes output files under the `data/` and `logs/` directories.

## GitHub Workflow

The workflow file `.github/workflows/daily-pipeline.yml.txt` schedules the pipeline to run every day. It performs the following steps:

1. Checks out the repository.
2. Sets up Python 3.10.
3. Installs dependencies using `requirements.txt`.
4. Runs `python scripts/run_pipeline.py`.
5. Uploads the `logs/failed_keywords_reparsed.json` artifact if any failures occurred.

Secrets for the environment variables must be configured in the repository settings to run the workflow successfully.

