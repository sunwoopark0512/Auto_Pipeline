# Auto Pipeline

This repository contains scripts for generating marketing hooks from trending keywords and uploading them to Notion. It uses OpenAI for text generation and Notion's API for storing results.

## Setup

1. Install Python 3.10 or higher.
2. Install dependencies. (The `requirements.txt` file is referenced in CI but is not included here. Install packages manually or create your own requirements file.)

```bash
pip install -r requirements.txt  # or install libraries manually
```

3. Create a `.env` file in the project root with the required environment variables described below.

## Environment Variables

| Variable | Description |
| --- | --- |
| `OPENAI_API_KEY` | OpenAI API key for generating content. |
| `NOTION_API_TOKEN` | Token for accessing the Notion API. |
| `NOTION_HOOK_DB_ID` | Database ID for storing generated hooks. |
| `NOTION_DB_ID` | Database ID for saving raw keyword metrics. Used by `scripts/notion_uploader.py`. |
| `NOTION_KPI_DB_ID` | Database ID for KPI tracking. |
| `KEYWORD_OUTPUT_PATH` | Path where keyword results are saved (default: `data/keyword_output_with_cpc.json`). |
| `HOOK_OUTPUT_PATH` | Path where generated hooks are saved (default: `data/generated_hooks.json`). |
| `FAILED_HOOK_PATH` | Path for storing failed hook generations (default: `logs/failed_hooks.json`). |
| `REPARSED_OUTPUT_PATH` | JSON file with items that failed to upload (default: `logs/failed_keywords_reparsed.json`). |
| `UPLOAD_DELAY` | Delay in seconds between Notion upload requests (default: `0.5`). |
| `RETRY_DELAY` | Delay in seconds between retry attempts (default: `0.5`). |
| `API_DELAY` | Delay in seconds between OpenAI API calls (default: `1.0`). |
| `UPLOADED_CACHE_PATH` | Cache file for uploaded keywords (default: `data/uploaded_keywords_cache.json`). |
| `FAILED_UPLOADS_PATH` | File used by `scripts/notion_uploader.py` to store failures (default: `logs/failed_uploads.json`). |
| `TOPIC_CHANNELS_PATH` | Path to `topic_channels.json` (default: `config/topic_channels.json`). |
| `SLACK_WEBHOOK_URL` | Optional: Slack webhook for notifications in GitHub Actions. |

## Usage

### Running Locally

1. Ensure the `.env` file is configured.
2. Run the full pipeline:

```bash
python run_pipeline.py
```

Individual scripts can also be executed:

```bash
python keyword_auto_pipeline.py       # collect trending keywords
python hook_generator.py              # generate marketing hooks using OpenAI
python notion_hook_uploader.py        # upload hooks to Notion
python retry_failed_uploads.py        # retry failed uploads
python retry_dashboard_notifier.py    # push KPI summary to Notion
```

### Running with GitHub Actions

A sample workflow is provided in `.github/workflows/daily-pipeline.yml.txt`. To enable it:

1. Rename the file to `daily-pipeline.yml`.
2. Add the required secrets to your repository settings:
   - `OPENAI_API_KEY`
   - `NOTION_API_TOKEN`
   - `NOTION_HOOK_DB_ID`
   - `NOTION_KPI_DB_ID`
   - `SLACK_WEBHOOK_URL` (optional)
3. The action runs daily via cron and can also be triggered manually.

The workflow checks out the repository, installs dependencies, and runs `python scripts/run_pipeline.py`. Adjust the path if your entrypoint differs.

