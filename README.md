# Auto Pipeline

A collection of scripts for generating trending keywords, creating marketing hooks using GPT, and uploading the results to Notion.

## Prerequisites

- **Python**: 3.10 or higher is recommended.
- **Dependencies**: install the required packages such as `openai`, `notion-client`, `python-dotenv`, `pytrends`, and `snscrape`.
- **Environment variables**: configure these in your environment or in a `.env` file:
  - `OPENAI_API_KEY` – OpenAI API key used by `hook_generator.py`.
  - `NOTION_API_TOKEN` – token for Notion API access.
  - `NOTION_DB_ID` – target Notion database for keyword uploads (used by `scripts/notion_uploader.py`).
  - `NOTION_HOOK_DB_ID` – Notion database where hooks are stored.
  - `NOTION_KPI_DB_ID` – database for dashboard statistics.
  - `KEYWORD_OUTPUT_PATH` – path for keyword JSON output. Defaults to `data/keyword_output_with_cpc.json`.
  - `HOOK_OUTPUT_PATH` – path for generated hooks. Defaults to `data/generated_hooks.json`.
  - `REPARSED_OUTPUT_PATH` – location of re-parsed/failed data. Defaults to `logs/failed_keywords_reparsed.json`.
  - `UPLOAD_DELAY`, `API_DELAY`, `RETRY_DELAY` – optional delay values between API calls or retries.

## Usage

Each script can be executed directly with Python:

```bash
python keyword_auto_pipeline.py        # Collect trending keywords
python hook_generator.py               # Generate hooks with GPT
python notion_hook_uploader.py         # Upload hooks to Notion
python retry_failed_uploads.py         # Retry failed uploads
python retry_dashboard_notifier.py     # Update KPI dashboard
```

The `scripts` directory contains additional helpers:

```bash
python scripts/notion_uploader.py      # Upload keyword data
python scripts/retry_failed_uploads.py # Retry failed Notion uploads
```

### Running the Full Pipeline

To execute the entire pipeline in sequence, run:

```bash
python run_pipeline.py
```

This calls the individual stages defined in `PIPELINE_SEQUENCE` and logs progress for each step.
