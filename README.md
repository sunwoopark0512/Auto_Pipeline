# Auto Pipeline

This repository contains scripts for generating keywords, creating content hooks using OpenAI, and uploading results to Notion. The pipeline can run locally or in CI.

## Environment Variables

The scripts rely on several environment variables. Configure them in a `.env` file or through the environment.

| Variable | Description |
| -------- | ----------- |
| `OPENAI_API_KEY` | API key for OpenAI used by `hook_generator.py`. |
| `NOTION_API_TOKEN` | Notion integration token required by upload and retry scripts. |
| `NOTION_DB_ID` | Database ID for keyword uploads (used in `scripts/notion_uploader.py`). |
| `NOTION_HOOK_DB_ID` | Database ID for generated hooks (`notion_hook_uploader.py` and retry scripts). |
| `NOTION_KPI_DB_ID` | Database ID for KPI dashboard (`retry_dashboard_notifier.py`). |
| `TOPIC_CHANNELS_PATH` | Path to `topic_channels.json` for keyword generation. |
| `KEYWORD_OUTPUT_PATH` | Path for keyword results consumed by multiple scripts. |
| `HOOK_OUTPUT_PATH` | Output path for generated hooks. |
| `FAILED_HOOK_PATH` | File for hooks that failed to generate. |
| `REPARSED_OUTPUT_PATH` | JSON file for failed keywords used by retry scripts. |
| `FAILED_UPLOADS_PATH` | File for failed Notion uploads. |
| `UPLOADED_CACHE_PATH` | Cache file of successfully uploaded keywords. |
| `UPLOAD_DELAY` | Delay in seconds between Notion uploads. |
| `API_DELAY` | Delay between OpenAI API calls. |
| `RETRY_DELAY` | Delay between retry attempts when uploading. |
| `SLACK_WEBHOOK_URL` | Webhook for CI notifications. |

## Running Locally

1. **Create a virtual environment** (Python 3.10 recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables** in a `.env` file or export them in your shell.

4. **Run the pipeline**:

   ```bash
   python run_pipeline.py
   ```

5. **Run tests** (if present):

   ```bash
   pytest
   ```

## Continuous Integration

The GitHub Actions workflow `daily-pipeline.yml.txt` runs the pipeline on a schedule. It installs dependencies, loads secrets for the environment variables above, and executes:

```bash
python scripts/run_pipeline.py
```

Failed keyword artifacts are uploaded at the end of the job for review.

