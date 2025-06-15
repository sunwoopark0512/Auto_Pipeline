# Auto Pipeline

This project automates the generation of marketing hooks and their upload to Notion.
The pipeline collects trending keywords, uses OpenAI to create hook sentences, and
stores the results in a Notion database. It is designed to run daily via GitHub
Actions but can also be executed manually with the provided scripts.

## Pipeline Overview

1. **Collect Keywords** (`keyword_auto_pipeline.py`)
   - Fetches trending topics from Google Trends and Twitter.
   - Filters keywords based on growth and mention thresholds.
   - Saves results to `KEYWORD_OUTPUT_PATH` (JSON).
2. **Generate Hooks** (`hook_generator.py`)
   - Uses OpenAI GPT to create hook sentences and content ideas for each keyword.
   - Results are written to `HOOK_OUTPUT_PATH`.
   - Failed items are stored at `FAILED_HOOK_PATH`.
3. **Upload to Notion** (`notion_hook_uploader.py`)
   - Uploads generated hooks to the Notion database defined by `NOTION_HOOK_DB_ID`.
   - Failed uploads are saved to `data/upload_failed_hooks.json`.
4. **Retry Failed Uploads** (`retry_failed_uploads.py`)
   - Attempts to re-upload items listed in `REPARSED_OUTPUT_PATH`.
5. **Dashboard Update** (`retry_dashboard_notifier.py`)
   - Summarises retry statistics and logs them to a KPI database.
6. **Orchestration** (`run_pipeline.py`)
   - Runs the above scripts in sequence.

The `.github/workflows/daily-pipeline.yml.txt` workflow executes this pipeline on a
schedule, installing dependencies and running `python scripts/run_pipeline.py`.
Artifacts of any failed uploads are uploaded for later inspection.

## Environment Variables

The pipeline relies on the following environment variables. Create a `.env` file or
use GitHub Actions secrets to provide these values.

- `OPENAI_API_KEY` – API key for OpenAI.
- `NOTION_API_TOKEN` – Token for accessing the Notion API.
- `NOTION_HOOK_DB_ID` – Database ID where hook results are stored.
- `NOTION_KPI_DB_ID` – Database ID for KPI metrics.
- `NOTION_DB_ID` – Generic Notion database ID for keyword uploads.
- `TOPIC_CHANNELS_PATH` – Path to the topic configuration JSON.
- `KEYWORD_OUTPUT_PATH` – Output path for collected keyword data.
- `HOOK_OUTPUT_PATH` – Output path for generated hooks.
- `FAILED_HOOK_PATH` – File path for failed hook generations.
- `REPARSED_OUTPUT_PATH` – File used for retrying failed uploads.
- `UPLOADED_CACHE_PATH` – Cache file for already uploaded keywords.
- `FAILED_UPLOADS_PATH` – File path for failed uploads log.
- `API_DELAY` – Delay (seconds) between OpenAI API calls.
- `UPLOAD_DELAY` – Delay (seconds) between Notion uploads.
- `RETRY_DELAY` – Delay (seconds) for retry operations.

## Example `.env` Template

See `.env.example` for a template. Copy it to `.env` and populate your secrets.

```bash
cp .env.example .env
```

## Running Scripts Manually

Activate your Python environment and run the desired stage:

```bash
python keyword_auto_pipeline.py
python hook_generator.py
python notion_hook_uploader.py
python retry_failed_uploads.py
python retry_dashboard_notifier.py
```

`run_pipeline.py` can be used to execute multiple steps automatically.

## GitHub Actions

The `Daily Notion Hook Pipeline` workflow triggers every day using cron. It
installs the project dependencies, runs the pipeline script, and uploads any failed
items as an artifact. A short summary is added to the workflow run for quick
reference.
