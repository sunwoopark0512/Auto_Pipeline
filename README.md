# Auto Pipeline

This repository contains a set of scripts that generate trending marketing hooks and upload them to Notion databases. The project automatically gathers trending keywords, creates hook sentences with OpenAI, and tracks the success of uploads.

## Project Goals

- Collect trending keywords from Google Trends and Twitter.
- Generate engaging hook sentences, blog post drafts and video title ideas using OpenAI.
- Upload the generated content to specific Notion databases.
- Retry failed uploads and log success metrics for monitoring.

## Pipeline Steps

1. **Keyword Collection (`keyword_auto_pipeline.py`)**
   - Gathers keywords for predefined topics.
   - Fetches metrics from Google Trends and Twitter.
   - Stores filtered results in `data/keyword_output_with_cpc.json`.

2. **Hook Generation (`hook_generator.py`)**
   - Loads keywords from the previous step.
   - Calls the OpenAI API to create marketing hooks and drafts.
   - Writes results to `data/generated_hooks.json`.

3. **Notion Upload (`notion_hook_uploader.py`)**
   - Uploads generated hooks into a Notion database.
   - Records any failures to `data/upload_failed_hooks.json`.

4. **Retry Failed Uploads (`retry_failed_uploads.py`)**
   - Attempts to upload any items that previously failed.

5. **KPI Update (`retry_dashboard_notifier.py`)**
   - Summarizes retry results and pushes a KPI entry to Notion.

Scripts can be run individually or in sequence via `run_pipeline.py`.

## Running Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and fill in the required values.
3. Execute the scripts in order:
   ```bash
   python keyword_auto_pipeline.py
   python hook_generator.py
   python notion_hook_uploader.py
   python retry_failed_uploads.py      # optional, only if there were failures
   python retry_dashboard_notifier.py  # update KPI dashboard
   ```
   Or run the bundled pipeline:
   ```bash
   python run_pipeline.py
   ```

## GitHub Actions Workflow

The workflow defined in `.github/workflows/daily-pipeline.yml.txt` runs the pipeline automatically every day and can also be triggered manually. It performs the following steps:

1. Check out the repository and set up Python 3.10.
2. Install dependencies listed in `requirements.txt`.
3. Run `python scripts/run_pipeline.py` to execute the full pipeline.
4. Upload a log of failed keywords as an artifact and append a summary to the workflow run.

Environment variables for the workflow are supplied through repository secrets and include API keys for OpenAI and Notion, as well as a Slack webhook URL for notifications.

