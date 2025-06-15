# Auto Pipeline

## Overview
This repository automates trending keyword discovery and Notion content updates.
The pipeline collects keywords, generates marketing hooks using OpenAI, uploads
them to Notion, and handles retries for failed uploads.

## Pipeline Steps
1. **Keyword collection** – `keyword_auto_pipeline.py` gathers trending keywords
   from Google Trends and Twitter and saves them to `KEYWORD_OUTPUT_PATH`.
2. **Hook generation** – `hook_generator.py` uses GPT to create hook sentences
   and blog/video drafts based on collected keywords. The output is stored in
   `HOOK_OUTPUT_PATH`.
3. **Notion upload** – `notion_hook_uploader.py` reads the generated hooks and
   creates pages in a Notion database specified by `NOTION_HOOK_DB_ID`.
4. **Retry processes** – `retry_failed_uploads.py` and
   `retry_dashboard_notifier.py` retry failed uploads and push KPI stats back to
   Notion.

## Environment Variables
| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | API key for OpenAI used when generating hooks. |
| `NOTION_API_TOKEN` | Token for authenticating to the Notion API. |
| `NOTION_HOOK_DB_ID` | Notion database ID where hooks are uploaded. |
| `NOTION_KPI_DB_ID` | Notion database ID for storing retry metrics. |
| `KEYWORD_OUTPUT_PATH` | Path to the keyword JSON file (default `data/keyword_output_with_cpc.json`). |
| `HOOK_OUTPUT_PATH` | Path to the generated hooks JSON (default `data/generated_hooks.json`). |
| `REPARSED_OUTPUT_PATH` | File used to store failed items that need retrying. |
| `TOPIC_CHANNELS_PATH` | Path to `topic_channels.json` for keyword topics. |
| `FAILED_HOOK_PATH` | Location to save failed GPT generations. |
| `FAILED_UPLOADS_PATH` | Where failed Notion uploads are stored. |
| `UPLOADED_CACHE_PATH` | Cache file for already uploaded keywords. |
| `NOTION_DB_ID` | Notion database ID used by `scripts/notion_uploader.py`. |
| `API_DELAY` | Delay between OpenAI API calls. |
| `UPLOAD_DELAY` | Delay between Notion uploads. |
| `RETRY_DELAY` | Delay between retry attempts. |
| `SLACK_WEBHOOK_URL` | Webhook URL for workflow notifications. |

## Running Locally
1. Install dependencies (Python 3.10 is recommended). Create a `.env` file and
   define the variables listed above.
2. Execute each step manually:
   ```bash
   python keyword_auto_pipeline.py
   python hook_generator.py
   python notion_hook_uploader.py
   python retry_failed_uploads.py
   python retry_dashboard_notifier.py
   ```
   or run the consolidated script:
   ```bash
   python run_pipeline.py
   ```

## GitHub Actions Workflow
A workflow definition is provided in
`.github/workflows/daily-pipeline.yml.txt`. Rename this file to
`daily-pipeline.yml` to enable the scheduled run. The workflow installs
dependencies, runs the pipeline via `python scripts/run_pipeline.py`, and uploads
any failure logs as artifacts.
