# Auto Pipeline

This repository contains a set of Python scripts that collect trending keywords, generate marketing hooks using GPT, and upload the results to Notion databases. The overall goal is to automate content generation and track retry statistics.

## Required environment variables

Set these variables in your environment or in a `.env` file before running the pipeline:

- `OPENAI_API_KEY` – OpenAI API key (e.g. `sk-xxxx`)
- `NOTION_API_TOKEN` – Notion integration token (e.g. `secret_xxxx`)
- `NOTION_DB_ID` – Notion database for raw keywords (e.g. `abc123def456`)
- `NOTION_HOOK_DB_ID` – Notion database for generated hooks (e.g. `abc123def456`)
- `NOTION_KPI_DB_ID` – Notion database for KPI metrics (e.g. `abc123def456`)
- `TOPIC_CHANNELS_PATH` – Path to `topic_channels.json` (default `config/topic_channels.json`)
- `KEYWORD_OUTPUT_PATH` – Output path for collected keywords (default `data/keyword_output_with_cpc.json`)
- `HOOK_OUTPUT_PATH` – Output path for generated hooks (default `data/generated_hooks.json`)
- `FAILED_HOOK_PATH` – Path to store failed hook generations (default `logs/failed_hooks.json`)
- `UPLOADED_CACHE_PATH` – Cache file for uploaded keywords (default `data/uploaded_keywords_cache.json`)
- `FAILED_UPLOADS_PATH` – File for upload failures (default `logs/failed_uploads.json`)
- `REPARSED_OUTPUT_PATH` – File for failed keywords to retry (default `logs/failed_keywords_reparsed.json`)
- `API_DELAY` – Delay between OpenAI API calls (default `1.0`)
- `UPLOAD_DELAY` – Delay between Notion uploads (default `0.5`)
- `RETRY_DELAY` – Delay between retry attempts (default `0.5`)

## Installation

Use Python 3.10 or later. Install dependencies with `pip`:

```bash
python -m pip install --upgrade pip
pip install openai notion-client python-dotenv pytrends snscrape
```

## Running the pipeline

Once the environment variables are configured and dependencies installed, run the pipeline from the project root:

```bash
python run_pipeline.py
```

The script executes the sequence defined in `run_pipeline.py`, calling the various helper scripts inside the `scripts/` directory. Logs and any failed items are written under the `logs/` folder.

