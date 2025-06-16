# Auto Pipeline

This repository contains a collection of scripts that gather trending keywords, generate short-form content hooks with GPT, and upload results to Notion. The pipeline can be triggered manually or through GitHub Actions.

## Requirements

- Python 3.10+
- The following Python packages:
  - `openai`
  - `python-dotenv`
  - `notion-client`
  - `pytrends`
  - `snscrape`

These packages can be installed with:

```bash
pip install -r requirements.txt
```

Alternatively, install them individually using `pip install package-name`.

## Environment Variables

The scripts rely on several environment variables. They can be placed in a `.env` file at the project root or configured in your shell environment.

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | API key used by `hook_generator.py` to call OpenAI. |
| `NOTION_API_TOKEN` | Notion integration token for uploading data. |
| `NOTION_HOOK_DB_ID` | Database ID for storing generated hooks. |
| `NOTION_DB_ID` | Database ID used by `scripts/notion_uploader.py`. |
| `NOTION_KPI_DB_ID` | Database ID for storing KPI summaries. |
| `KEYWORD_OUTPUT_PATH` | Path for keyword collection output (default `data/keyword_output_with_cpc.json`). |
| `HOOK_OUTPUT_PATH` | Path for generated hook JSON (default `data/generated_hooks.json`). |
| `FAILED_HOOK_PATH` | Path where failed hook generations are stored. |
| `UPLOADED_CACHE_PATH` | File used to cache successfully uploaded keywords. |
| `FAILED_UPLOADS_PATH` | File that stores failed keyword uploads. |
| `REPARSED_OUTPUT_PATH` | Location of parsed failed items for retry attempts. |
| `UPLOAD_DELAY` | Delay between Notion uploads in seconds (default `0.5`). |
| `API_DELAY` | Delay between OpenAI API calls in seconds. |
| `RETRY_DELAY` | Delay when retrying failed uploads. |
| `TOPIC_CHANNELS_PATH` | JSON list of main topics (`config/topic_channels.json`). |

## Script Overview

### `keyword_auto_pipeline.py`
Collects trending keywords from Google Trends and Twitter. Filters them based on score, growth, mentions, and CPC before saving to `KEYWORD_OUTPUT_PATH`.
Example output snippet:
```json
{
  "filtered_keywords": [
    {"keyword": "여행 국내여행", "source": "GoogleTrends", "score": 78, "growth": 1.4, "cpc": 1500}
  ]
}
```

### `hook_generator.py`
Generates marketing hooks, blog drafts, and YouTube title ideas from keywords using GPT-4. Results are written to `HOOK_OUTPUT_PATH` and failures to `FAILED_HOOK_PATH`.

### `notion_hook_uploader.py`
Uploads generated hooks to the Notion database specified by `NOTION_HOOK_DB_ID`. Skips duplicates and records failures for later retry.

### `retry_failed_uploads.py`
Attempts to re-upload any items listed under `REPARSED_OUTPUT_PATH`. Remaining failures are overwritten to the same file.

### `retry_dashboard_notifier.py`
Summarizes retry results and pushes KPI metrics (total attempts, successes, failures) to the database specified by `NOTION_KPI_DB_ID`.

### `run_pipeline.py`
Orchestrates the entire workflow. By default it executes:
1. `hook_generator.py`
2. `parse_failed_gpt.py`
3. `retry_failed_uploads.py`
4. `notify_retry_result.py`
5. `retry_dashboard_notifier.py`

Each stage prints log messages similar to:
```
2025-06-16 00:55:15,465 INFO:🧩 파이프라인 시작: 2025-06-16 00:55
2025-06-16 00:55:15,465 ERROR:❌ 파일이 존재하지 않습니다: scripts/hook_generator.py
```

### `scripts/notion_uploader.py`
Legacy helper used to upload raw keywords directly to Notion. Maintains a cache to avoid duplicates.

### `scripts/retry_failed_uploads.py`
Older retry implementation for hook uploads. Functions similarly to the root `retry_failed_uploads.py` script.

## Running Manually

1. Install dependencies and prepare your `.env` file with all required variables.
2. Execute the pipeline:
   ```bash
   python run_pipeline.py
   ```
   Logs are printed to the console and saved under the `logs/` directory.

## Running with GitHub Actions

A workflow file is provided in `.github/workflows/daily-pipeline.yml.txt`. It installs dependencies, runs the pipeline, uploads any failed items, and appends a summary.

To trigger the workflow manually, navigate to the **Actions** tab on GitHub and choose the *workflow_dispatch* option. The pipeline also runs daily via a cron schedule.

