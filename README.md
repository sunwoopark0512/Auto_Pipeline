# Auto Pipeline

This repository contains a set of scripts to collect trending keywords, generate marketing hooks using GPT models and upload the results to Notion. The main entrypoint is `run_pipeline.py` which orchestrates the different stages.

## Environment variables

The pipeline relies on several environment variables. They can be provided via a `.env` file or exported in the shell before running the scripts.

Required variables:

- `OPENAI_API_KEY` – API key used by `hook_generator.py` to call OpenAI.
- `NOTION_API_TOKEN` – token for the Notion API.
- `NOTION_DB_ID` – database ID for the keyword list (used by `notion_uploader.py`).
- `NOTION_HOOK_DB_ID` – database for storing generated hooks.
- `NOTION_KPI_DB_ID` – database for KPI stats pushed by `retry_dashboard_notifier.py`.

Optional variables with defaults:

- `TOPIC_CHANNELS_PATH` – path to the topic configuration (default: `config/topic_channels.json`).
- `KEYWORD_OUTPUT_PATH` – JSON file where filtered keywords are stored (default: `data/keyword_output_with_cpc.json`).
- `HOOK_OUTPUT_PATH` – JSON file for generated hooks (default: `data/generated_hooks.json`).
- `FAILED_HOOK_PATH` – log file for failed GPT generations (default: `logs/failed_hooks.json`).
- `FAILED_UPLOADS_PATH` – log file for failed keyword uploads (default: `logs/failed_uploads.json`).
- `UPLOADED_CACHE_PATH` – cache for already uploaded keywords (default: `data/uploaded_keywords_cache.json`).
- `REPARSED_OUTPUT_PATH` – location of data for retry processing (default: `logs/failed_keywords_reparsed.json`).
- `API_DELAY` – delay between OpenAI API calls (default: `1.0`).
- `UPLOAD_DELAY` – delay between Notion uploads (default: `0.5`).
- `RETRY_DELAY` – delay between retry attempts (default: `0.5`).

## Running the pipeline

1. Install the required Python packages.
2. Set the environment variables above.
3. Execute the full pipeline:

```bash
python run_pipeline.py
```

Individual steps can also be executed directly:

```bash
python keyword_auto_pipeline.py     # collect keywords
python hook_generator.py            # generate hooks via OpenAI
python notion_hook_uploader.py      # upload hooks to Notion
```

## Tests and linters

Unit tests can be executed with `pytest`:

```bash
pytest
```

To run linters use `pylint`:

```bash
pylint *.py scripts/*.py
```

Make sure all tests pass and the linter reports no issues before committing changes.
