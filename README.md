# Auto Pipeline

This repository contains an automated pipeline that collects trending keywords, generates marketing hooks using OpenAI, and uploads the results to Notion. The pipeline can be executed manually on your machine or scheduled through GitHub Actions.

## Requirements

1. Python 3.10+
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Required Environment Variables

Set the following variables in your environment or in a `.env` file before running the scripts:

- `OPENAI_API_KEY` – API key for OpenAI.
- `NOTION_API_TOKEN` – token used to access the Notion API.
- `NOTION_HOOK_DB_ID` – database ID where generated hooks are stored.
- `NOTION_KPI_DB_ID` – database ID for logging retry statistics.
- `NOTION_DB_ID` – database ID for saving collected keyword metrics.
- `KEYWORD_OUTPUT_PATH` – path to save collected keyword data (default: `data/keyword_output_with_cpc.json`).
- `HOOK_OUTPUT_PATH` – path to save generated hooks (default: `data/generated_hooks.json`).
- `FAILED_HOOK_PATH` – path for hooks that failed to generate (default: `logs/failed_hooks.json`).
- `REPARSED_OUTPUT_PATH` – path used when retrying failed uploads (default: `logs/failed_keywords_reparsed.json`).
- `UPLOAD_DELAY` – delay in seconds between Notion uploads (default: `0.5`).
- `RETRY_DELAY` – delay in seconds between retry attempts (default: `0.5`).

## Running Manually

You can execute each stage individually or run the orchestrated pipeline.

### Individual scripts

```bash
python keyword_auto_pipeline.py     # Collect trending keywords
python hook_generator.py            # Generate hook content using GPT-4
python notion_hook_uploader.py      # Upload hooks to Notion
python retry_failed_uploads.py      # Retry failed uploads
python retry_dashboard_notifier.py  # Update KPI dashboard with retry stats
```

### Full pipeline

The `run_pipeline.py` script runs the above steps in sequence:

```bash
python run_pipeline.py
```

## GitHub Actions

The workflow `.github/workflows/daily-pipeline.yml.txt` runs the pipeline daily using GitHub Actions. Secrets must be configured in the repository settings with the same names as the environment variables listed above. The action installs dependencies via `pip install -r requirements.txt` and then executes the pipeline.


