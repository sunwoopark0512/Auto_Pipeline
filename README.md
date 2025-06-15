# Auto Pipeline

This repository automates collecting trending keywords, generating marketing hooks using GPT, and uploading results to Notion.

## Overview

1. `keyword_auto_pipeline.py` &mdash; Fetches trending keywords from Google Trends and Twitter, filters them and saves `data/keyword_output_with_cpc.json`.
2. `hook_generator.py` &mdash; Generates hook sentences, blog draft and YouTube titles for each keyword using OpenAI. Output stored in `data/generated_hooks.json`.
3. `notion_hook_uploader.py` &mdash; Uploads generated hooks to a Notion database.
4. `retry_failed_uploads.py` &mdash; Attempts to upload items that failed previously.
5. `retry_dashboard_notifier.py` &mdash; Updates KPI statistics in a Notion dashboard.
6. `run_pipeline.py` &mdash; Runs the above scripts sequentially.
7. Additional helper scripts live in the `scripts/` directory.

## Setup

Create a `.env` file in the project root and define at least:

```
OPENAI_API_KEY=your-openai-key
NOTION_API_TOKEN=your-notion-token
NOTION_HOOK_DB_ID=your-notion-database-id
```

Other optional variables include `NOTION_KPI_DB_ID`, `NOTION_DB_ID`, `KEYWORD_OUTPUT_PATH`, `HOOK_OUTPUT_PATH` and more. See each script for defaults.

## Installation

```bash
python3 -m pip install --upgrade pip
pip install openai python-dotenv notion-client pytrends snscrape
```

## Running the pipeline

Run everything locally via:

```bash
python run_pipeline.py
```

or execute individual scripts as needed.

A GitHub Actions workflow (`.github/workflows/daily-pipeline.yml.txt`) is provided for scheduled execution. Rename the file to `daily-pipeline.yml` and configure the necessary repository secrets (`OPENAI_API_KEY`, `NOTION_API_TOKEN`, `NOTION_HOOK_DB_ID`, etc.) to enable automated runs.

