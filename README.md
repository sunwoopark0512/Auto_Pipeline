# Auto Pipeline

This repository contains a set of Python scripts that collect trending keywords,
create marketing hooks using OpenAI and upload the results to Notion.
The project can be executed locally or scheduled through GitHub Actions.

## Setup

1. **Python**: Install Python 3.10 or later.
2. **Dependencies**: Install required packages:
   ```bash
   pip install openai notion-client python-dotenv pytrends snscrape
   ```
   Additional packages may be required depending on your environment.
3. **Environment file**: Copy `.env.example` to `.env` and fill in the values.
   ```bash
   cp .env.example .env
   ```

## Required Environment Variables

The main variables used by the scripts are shown below. Default paths are
provided in the example file.

- `OPENAI_API_KEY` – API key for generating text with OpenAI.
- `NOTION_API_TOKEN` – Token for accessing the Notion API.
- `NOTION_DB_ID` – Database ID used when uploading keyword metrics.
- `NOTION_HOOK_DB_ID` – Database ID for uploading generated hooks.
- `NOTION_KPI_DB_ID` – Database used by the retry dashboard notifier.
- `SLACK_WEBHOOK_URL` – Optional Slack webhook used in the GitHub Action.
- `TOPIC_CHANNELS_PATH`, `KEYWORD_OUTPUT_PATH`, `HOOK_OUTPUT_PATH`,
  `FAILED_HOOK_PATH`, `REPARSED_OUTPUT_PATH`, `UPLOADED_CACHE_PATH`,
  `FAILED_UPLOADS_PATH` – File locations for intermediate results.
- `API_DELAY`, `UPLOAD_DELAY`, `RETRY_DELAY` – Timing parameters for API calls
  and uploads.

See `.env.example` for the full list and default values.

## Basic Usage

1. **Collect trending keywords**
   ```bash
   python keyword_auto_pipeline.py
   ```
   This creates a JSON file with filtered keywords.

2. **Generate marketing hooks**
   ```bash
   python hook_generator.py
   ```
   The script reads the keyword file and produces hook lines, blog drafts and
   video titles using OpenAI.

3. **Upload hooks to Notion**
   ```bash
   python notion_hook_uploader.py
   ```
   Failed uploads are recorded and can be retried later using
   `retry_failed_uploads.py` or `scripts/retry_failed_uploads.py`.

4. **Run the whole pipeline**
   ```bash
   python run_pipeline.py
   ```
   `run_pipeline.py` executes several of the scripts above in order.

An example GitHub Actions workflow is available in
`.github/workflows/daily-pipeline.yml.txt` which shows how the pipeline can be
scheduled daily.
