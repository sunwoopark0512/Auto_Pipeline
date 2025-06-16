# Auto Pipeline

This repository contains a collection of small scripts that generate marketing hooks using OpenAI, upload them to Notion and keep track of failed uploads. The scripts are orchestrated by `run_pipeline.py`.

## Requirements

Python 3.10 or later is recommended. Install the required packages:

```bash
pip install openai notion-client python-dotenv pytrends snscrape
```

You can also store them in `requirements.txt` and install via `pip install -r requirements.txt`.

## Environment Variables

The scripts rely on several environment variables. Create a `.env` file in the project root or export them in your environment before running the pipeline.

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | API key for OpenAI GPT. Required by `hook_generator.py`. |
| `NOTION_API_TOKEN` | Notion integration token. |
| `NOTION_HOOK_DB_ID` | Notion database ID used to store generated hooks. |
| `NOTION_DB_ID` | Database ID used by `scripts/notion_uploader.py` for keyword data. |
| `NOTION_KPI_DB_ID` | Database ID for KPI stats in `retry_dashboard_notifier.py`. |
| `KEYWORD_OUTPUT_PATH` | Location of keyword JSON produced by `keyword_auto_pipeline.py`. Default: `data/keyword_output_with_cpc.json`. |
| `HOOK_OUTPUT_PATH` | JSON file path where generated hooks are stored. |
| `FAILED_HOOK_PATH` | File path for saving failed hook generations. |
| `REPARSED_OUTPUT_PATH` | Path of the file containing re-parsed failed hooks. |
| `UPLOAD_DELAY` | Delay between Notion upload calls (seconds). |
| `RETRY_DELAY` | Delay between retry attempts when uploading failed hooks. |
| `API_DELAY` | Delay between OpenAI API calls. |
| `TOPIC_CHANNELS_PATH` | Path to the topic configuration JSON. |
| `UPLOADED_CACHE_PATH` | Cache file to avoid re-uploading to Notion. |
| `FAILED_UPLOADS_PATH` | File where failed keyword uploads are written. |

## Running the Pipeline

Run all steps locally with:

```bash
python run_pipeline.py
```

This sequentially executes:

1. `hook_generator.py` – create marketing hooks from keywords using GPT-4.
2. `parse_failed_gpt.py` – parse hooks that failed to generate (script not present in repository).
3. `retry_failed_uploads.py` – retry uploading failed items to Notion.
4. `notify_retry_result.py` – post a summary notification (script not present in repository).
5. `retry_dashboard_notifier.py` – upload KPI data to Notion.

Only the scripts present in this repository will run successfully. Missing scripts can be implemented following the same pattern.

## Script Overview

### `keyword_auto_pipeline.py`
Collect trending keywords from Google Trends and Twitter. The result is saved to the file specified by `KEYWORD_OUTPUT_PATH`.

### `hook_generator.py`
Read the keywords JSON and generate hook sentences using OpenAI GPT-4. Results are stored in `HOOK_OUTPUT_PATH`. Failed generations are logged to `FAILED_HOOK_PATH`.

### `scripts/notion_uploader.py`
Upload keyword metrics from the Google/Twitter step to a Notion database specified by `NOTION_DB_ID`. Uses an upload cache and records failed items.

### `notion_hook_uploader.py`
Push generated hooks to another Notion database defined by `NOTION_HOOK_DB_ID`.

### `scripts/retry_failed_uploads.py`
Retry uploading any failed hooks stored in `FAILED_HOOK_PATH`.

### `retry_dashboard_notifier.py`
Summarise retry statistics from `REPARSED_OUTPUT_PATH` and insert a KPI row into `NOTION_KPI_DB_ID`.

### `run_pipeline.py`
Simple orchestrator that runs the scripts in `PIPELINE_SEQUENCE`. Adjust the sequence to match the scripts available in your repository.

## GitHub Actions

A sample workflow is located at `.github/workflows/daily-pipeline.yml.txt`. Rename it to `daily-pipeline.yml` to enable it on GitHub. The job installs dependencies, executes the pipeline and uploads the failed hooks JSON as an artifact. Environment variables are read from repository secrets:

```yaml
env:
  OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
  NOTION_API_TOKEN: ${{ secrets.NOTION_API_TOKEN }}
  NOTION_HOOK_DB_ID: ${{ secrets.NOTION_HOOK_DB_ID }}
  NOTION_KPI_DB_ID: ${{ secrets.NOTION_KPI_DB_ID }}
```

Edit the cron schedule or workflow steps as needed.

---

Feel free to extend or modify these scripts for your automation needs.
