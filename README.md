# Auto Pipeline

Auto Pipeline is a collection of scripts that gather trending keywords, generate marketing hooks with OpenAI and upload the results to Notion.  The `run_pipeline.py` script acts as an orchestrator for running the individual steps in order.

## Overview

The typical flow is:

1. `keyword_auto_pipeline.py` collects trending keywords from Google Trends and Twitter.
2. `hook_generator.py` uses GPT-4 to generate hook sentences, blog drafts and video title suggestions for each keyword.
3. `notion_hook_uploader.py` uploads the generated hooks to a Notion database.
4. `retry_failed_uploads.py` and `retry_dashboard_notifier.py` handle failed uploads and update a Notion KPI dashboard.

Running `run_pipeline.py` will execute these scripts sequentially.

## Environment variables

Create a `.env` file or configure the following variables in your environment before running any script:

- `OPENAI_API_KEY` – API key used by `hook_generator.py`.
- `NOTION_API_TOKEN` – token for the Notion API used by uploader and retry scripts.
- `NOTION_HOOK_DB_ID` – ID of the Notion database that stores generated hooks.
- `NOTION_KPI_DB_ID` – database ID for KPI tracking in `retry_dashboard_notifier.py`.
- `NOTION_DB_ID` – database used by `scripts/notion_uploader.py` when uploading keyword data.
- `TOPIC_CHANNELS_PATH` – optional path for the topic configuration JSON (defaults to `config/topic_channels.json`).
- `KEYWORD_OUTPUT_PATH` – location to store the keyword output JSON file.
- `HOOK_OUTPUT_PATH` – location to save generated hooks.
- `FAILED_HOOK_PATH` – file where failed hook generations are recorded.
- `REPARSED_OUTPUT_PATH` – JSON file for parsed or retried data.
- `UPLOADED_CACHE_PATH` – cache used by the Notion uploader to avoid duplicates.
- `FAILED_UPLOADS_PATH` – path for storing failed uploads from `scripts/notion_uploader.py`.
- `UPLOAD_DELAY` – delay in seconds between Notion uploads.
- `RETRY_DELAY` – delay used when retrying failed uploads.
- `API_DELAY` – delay between OpenAI API calls.

Other environment variables such as `SLACK_WEBHOOK_URL` may be required if you enable notifications via the GitHub Actions workflow.

## Local usage

Install Python dependencies (for example with `pip install openai notion-client pytrends snscrape python-dotenv`) and ensure your `.env` file is populated.  Then run:

```bash
python run_pipeline.py
```

This will invoke each script listed in `PIPELINE_SEQUENCE` inside `run_pipeline.py`.

## GitHub workflow

The repository contains a workflow file at `.github/workflows/daily-pipeline.yml.txt` which runs the pipeline on a schedule (daily at 00:00 UTC, corresponding to 09:00 KST) or can be triggered manually from the Actions tab.  The workflow exposes the same environment variables via GitHub secrets and executes `python scripts/run_pipeline.py`.

To run the workflow manually, open the GitHub Actions page for this repository, select **Daily Notion Hook Pipeline** and click **Run workflow**.  Scheduled runs happen automatically once per day.

