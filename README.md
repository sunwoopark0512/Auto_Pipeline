# Auto Pipeline

This repository contains a small collection of scripts that gather trending keywords, generate marketing hooks with OpenAI, and upload the results to Notion. The provided GitHub Actions workflow can execute the full pipeline on a schedule.

## Pipeline stages

1. **`keyword_auto_pipeline.py`** – Collects trending keywords from Google Trends and Twitter and saves them to `data/keyword_output_with_cpc.json`.
2. **`hook_generator.py`** – Uses the keywords to generate short hooks and summaries via the OpenAI API. Results are stored in `data/generated_hooks.json`.
3. **`notion_hook_uploader.py`** – Uploads the generated hooks to the configured Notion database.
4. **`retry_failed_uploads.py`** – Attempts to re‑upload any failed items recorded in `logs/failed_keywords_reparsed.json`.
5. **`retry_dashboard_notifier.py`** – Pushes a KPI summary of retry results to another Notion database.
6. **`run_pipeline.py`** – Utility script that sequentially executes the above stages.

## Required environment variables

The scripts read configuration from environment variables (usually via a `.env` file):

- `OPENAI_API_KEY` – API key for the OpenAI API.
- `NOTION_API_TOKEN` – Notion integration token.
- `NOTION_HOOK_DB_ID` – Database ID where hooks will be stored.
- `NOTION_KPI_DB_ID` – Database ID for logging KPI metrics.
- `NOTION_DB_ID` – Database ID for uploading raw keywords (used by `scripts/notion_uploader.py`).
- `HOOK_OUTPUT_PATH` – Path to the generated hooks JSON file (default `data/generated_hooks.json`).
- `FAILED_HOOK_PATH` – Path to store hooks that failed generation (default `logs/failed_hooks.json`).
- `REPARSED_OUTPUT_PATH` – JSON file containing failed uploads that should be retried.
- `KEYWORD_OUTPUT_PATH` – Location of the collected keyword file.
- `UPLOAD_DELAY`, `RETRY_DELAY`, `API_DELAY` – Optional delay values used between API calls.
- `SLACK_WEBHOOK_URL` – Slack webhook used in the GitHub Actions workflow.

## Example `.env`

```env
OPENAI_API_KEY=sk-...
NOTION_API_TOKEN=secret_...
NOTION_HOOK_DB_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_KPI_DB_ID=yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
NOTION_DB_ID=zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
```

## Installation

1. Clone the repository and move into it.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the pipeline locally

1. Ensure all required environment variables are available (or create a `.env` file).
2. Execute the pipeline with:

```bash
python run_pipeline.py
```

Individual stages can also be run directly by calling the corresponding script.

## Tests

Run unit tests with:

```bash
pytest
```

(There are currently no tests bundled with this repository.)

## GitHub Actions

The workflow defined in `.github/workflows/daily-pipeline.yml.txt` executes the full pipeline every day at 09:00 KST. It can also be triggered manually from the **Actions** tab using the **Run workflow** button.

