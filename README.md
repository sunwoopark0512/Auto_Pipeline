# Auto Pipeline

This repository automates generation of trending marketing hooks and uploads them to Notion databases.

## Overview

1. **keyword_auto_pipeline.py** – Collect trending keywords from Google Trends and Twitter.
2. **hook_generator.py** – Use GPT to generate hook sentences, blog draft paragraphs and YouTube titles.
3. **notion_hook_uploader.py** – Upload generated hooks to a Notion database.
4. **retry_failed_uploads.py / scripts/retry_failed_uploads.py** – Retry failed Notion uploads.
5. **retry_dashboard_notifier.py** – Push KPI metrics of retries to another Notion database.
6. **run_pipeline.py** – Orchestrate the pipeline by running the above scripts in order.

## Setup

1. Create a `.env` file based on `.env.example` and provide required tokens and IDs.
2. Install Python 3.10 or higher and required packages:
   ```bash
   pip install openai notion-client python-dotenv pytrends snscrape
   ```

## Environment Variables

The following variables configure the pipeline:

- `OPENAI_API_KEY` – API key for OpenAI.
- `NOTION_API_TOKEN` – Notion integration token.
- `NOTION_HOOK_DB_ID` – Database ID where generated hooks are stored.
- `NOTION_DB_ID` – Database ID for storing keyword metrics.
- `NOTION_KPI_DB_ID` – Database ID for retry statistics.
- `TOPIC_CHANNELS_PATH` – Path to topic configuration JSON (default `config/topic_channels.json`).
- `KEYWORD_OUTPUT_PATH` – JSON file path for collected keywords (default `data/keyword_output_with_cpc.json`).
- `HOOK_OUTPUT_PATH` – JSON file path for generated hooks (default `data/generated_hooks.json`).
- `FAILED_HOOK_PATH` – Output path for failed hook generations.
- `UPLOADED_CACHE_PATH` – Cache file for uploaded keywords.
- `FAILED_UPLOADS_PATH` – File storing uploads that failed.
- `REPARSED_OUTPUT_PATH` – File containing failed items that were reparsed.
- `UPLOAD_DELAY` – Delay between Notion uploads in seconds.
- `API_DELAY` – Delay between OpenAI API calls.
- `RETRY_DELAY` – Delay between retry attempts in seconds.
- `SLACK_WEBHOOK_URL` – Optional Slack webhook for notifications.

## Running the Pipeline

Execute the full pipeline locally:

```bash
python run_pipeline.py
```

Each script can also be run individually if needed. Logs and any failed items are written under the `logs/` directory.

## Scheduling

The project includes a GitHub Actions workflow (`.github/workflows/daily-pipeline.yml.txt`) that runs the pipeline daily. You can adapt this file or use your own cron job to schedule `python run_pipeline.py` at your desired interval.
