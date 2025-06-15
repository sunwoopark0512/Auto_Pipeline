# Auto Pipeline

This repository contains automation scripts that collect trending keywords, generate marketing hooks using GPT, and upload them to Notion. Failed uploads are retried automatically and summarized in a KPI dashboard.

## Pipeline Overview

1. **Keyword Collection** (`keyword_auto_pipeline.py`)
   - Fetches data from Google Trends and Twitter.
   - Outputs to the file defined by `KEYWORD_OUTPUT_PATH`.
2. **Hook Generation** (`hook_generator.py`)
   - Uses OpenAI to create short-form hooks and related text.
   - Reads keywords from `KEYWORD_OUTPUT_PATH` and writes results to `HOOK_OUTPUT_PATH`.
3. **Notion Upload** (`notion_hook_uploader.py`)
   - Uploads generated hooks to the Notion database specified by `NOTION_HOOK_DB_ID`.
   - Stores any failures for later retries.
4. **Retry Logic** (`retry_failed_uploads.py` & `retry_dashboard_notifier.py`)
   - Attempts to re-upload items listed in `REPARSED_OUTPUT_PATH`.
   - Reports retry metrics to the database given by `NOTION_KPI_DB_ID`.

All steps can be executed sequentially via `run_pipeline.py`.

## Environment Variables

| Variable | Description |
| --- | --- |
| `OPENAI_API_KEY` | OpenAI key for generating hooks. |
| `NOTION_API_TOKEN` | Authentication token for the Notion API. |
| `NOTION_HOOK_DB_ID` | ID of the Notion database used to store hooks. |
| `NOTION_KPI_DB_ID` | Notion database for retry statistics. |
| `NOTION_DB_ID` | Database used by the legacy keyword uploader script. |
| `KEYWORD_OUTPUT_PATH` | JSON file path where collected keywords are stored. |
| `HOOK_OUTPUT_PATH` | Path where generated hooks are written. |
| `FAILED_HOOK_PATH` | File to log hook generation failures. |
| `REPARSED_OUTPUT_PATH` | JSON file of items that need to be retried. |
| `TOPIC_CHANNELS_PATH` | Optional topic configuration for keyword collection. |
| `UPLOADED_CACHE_PATH` | Cache path while uploading keywords. |
| `FAILED_UPLOADS_PATH` | Log path for Notion upload failures. |
| `UPLOAD_DELAY` | Delay between Notion upload requests. |
| `RETRY_DELAY` | Delay between retry attempts. |
| `API_DELAY` | Delay between OpenAI API calls. |

Default values for the paths and delays are defined in each script.

## Running Locally

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file and populate it with the environment variables listed above.
3. Run the full pipeline:
   ```bash
   python run_pipeline.py
   ```
   Each stage prints its progress to the console.

## GitHub Actions

The workflow `.github/workflows/daily-pipeline.yml.txt` runs the pipeline on a schedule and can be triggered manually. It checks out the repository, installs dependencies, and executes:

```yaml
- name: ▶️ Run full pipeline (single entrypoint)
  run: python scripts/run_pipeline.py
```

Failed items are uploaded as an artifact and a brief summary is appended to the workflow run.
