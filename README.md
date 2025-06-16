# Auto Pipeline

This repository provides a collection of Python scripts for generating marketing hooks from trending keywords and uploading the results to Notion. The project also includes a GitHub workflow for running the pipeline automatically.

## Installation

1. Install Python 3.10 or higher.
2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file or export the following variables before running the scripts. Only the variables used by each script are required.

- `OPENAI_API_KEY` – OpenAI API token used by `hook_generator.py`.
- `NOTION_API_TOKEN` – Notion integration token used by uploader scripts.
- `NOTION_HOOK_DB_ID` – ID of the Notion database that stores generated hooks.
- `NOTION_DB_ID` – ID of the Notion database used by `scripts/notion_uploader.py`.
- `NOTION_KPI_DB_ID` – ID of the Notion database that stores retry KPIs.
- `KEYWORD_OUTPUT_PATH` – Path for keyword data (default: `data/keyword_output_with_cpc.json`).
- `HOOK_OUTPUT_PATH` – Path for generated hooks JSON (default: `data/generated_hooks.json`).
- `FAILED_HOOK_PATH` – Path for hooks that failed generation (default: `logs/failed_hooks.json`).
- `REPARSED_OUTPUT_PATH` – Path for failed keyword data used in retries (default: `logs/failed_keywords_reparsed.json`).
- `UPLOAD_DELAY` – Delay between Notion uploads.
- `API_DELAY` – Delay between OpenAI API calls.
- `RETRY_DELAY` – Delay between retry attempts.
- `TOPIC_CHANNELS_PATH` – Topic list for the keyword pipeline (default: `config/topic_channels.json`).
- `UPLOADED_CACHE_PATH` – Cache file used by `scripts/notion_uploader.py`.
- `FAILED_UPLOADS_PATH` – Log path for failed uploads from `scripts/notion_uploader.py`.

## Script Overview

| Script | Purpose |
|-------|---------|
| `keyword_auto_pipeline.py` | Collect trending keywords from Google Trends and Twitter and save them to a JSON file. |
| `hook_generator.py` | Use OpenAI to generate hooks based on the filtered keywords. |
| `notion_hook_uploader.py` | Upload the generated hooks to a Notion database. |
| `retry_failed_uploads.py` | Retry uploading hooks that previously failed. |
| `retry_dashboard_notifier.py` | Update a KPI dashboard in Notion with retry statistics. |
| `run_pipeline.py` | Execute multiple scripts in sequence. |
| `scripts/notion_uploader.py` | Upload raw keyword metrics to a Notion database. |
| `scripts/retry_failed_uploads.py` | Retry failed hook uploads using a different log file. |

### Running the Pipeline

Execute the pipeline locally after setting the required environment variables:

```bash
python run_pipeline.py
```

Individual scripts can also be run directly using the same command pattern.

## GitHub Workflow

The file `.github/workflows/daily-pipeline.yml.txt` defines a workflow that installs dependencies and runs the pipeline once per day. To enable it:

1. Add the required tokens as GitHub secrets:
   - `OPENAI_API_KEY`
   - `NOTION_API_TOKEN`
   - `NOTION_HOOK_DB_ID`
   - `NOTION_KPI_DB_ID`
   - `SLACK_WEBHOOK_URL`
2. The workflow checks out the repository, installs packages from `requirements.txt`, and executes `python scripts/run_pipeline.py`.
3. Failed keywords are uploaded as an artifact and summarized in the workflow summary.

