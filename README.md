# Auto Pipeline

This repository contains a collection of Python scripts that build marketing hooks from trending keywords and upload them to Notion. Keywords are gathered from Google Trends and Twitter, then fed to OpenAI GPT to generate hook sentences and blog/YouTube ideas. Generated results are uploaded to specific Notion databases.

## Requirements

Install Python 3.10+ and the packages listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

## Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

- `OPENAI_API_KEY` – API key for OpenAI models.
- `NOTION_API_TOKEN` – Notion integration token with access to the target databases.
- `NOTION_HOOK_DB_ID` – Database ID where generated hooks are stored.
- `NOTION_KPI_DB_ID` – Database ID for logging KPI information.
- `NOTION_DB_ID` – Database ID for storing raw keyword metrics.
- `SLACK_WEBHOOK_URL` – Slack webhook used by GitHub Actions (optional).
- `REPARSED_OUTPUT_PATH` – Path for storing failed keyword information.
- `KEYWORD_OUTPUT_PATH` – JSON output from `keyword_auto_pipeline.py`.
- `HOOK_OUTPUT_PATH` – File used by `hook_generator.py` and `notion_hook_uploader.py`.
- `FAILED_HOOK_PATH` – Location to store failed hook generations.
- `FAILED_UPLOADS_PATH` – Path for failed uploads from `notion_uploader.py`.
- `UPLOADED_CACHE_PATH` – Cache of already uploaded keywords.
- `UPLOAD_DELAY`, `API_DELAY`, `RETRY_DELAY` – Optional delay settings for API calls.
- `TOPIC_CHANNELS_PATH` – Path to the topic configuration JSON.

## Running Locally

1. Ensure `.env` is configured with the variables above.
2. Execute the combined pipeline:

```bash
python run_pipeline.py
```

The pipeline sequentially runs the scripts in `PIPELINE_SEQUENCE` defined in `run_pipeline.py`.

## GitHub Actions

A workflow file in `.github/workflows/daily-pipeline.yml.txt` runs the same pipeline on a schedule. Secrets in your GitHub repository must supply the environment variables listed above.

