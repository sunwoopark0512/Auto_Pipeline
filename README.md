# Auto Pipeline

Auto Pipeline collects trending keywords, generates marketing hook content, and uploads the results to Notion. It can be run manually or scheduled through GitHub Actions.

## Installation

1. Create and activate a Python 3.10 environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Required Environment Variables

Set these variables in a `.env` file or as environment variables before running the pipeline:

- **OPENAI_API_KEY** – API key for generating text.
- **NOTION_API_TOKEN** – token for the Notion API.
- **NOTION_HOOK_DB_ID** – Notion database ID for storing generated hooks.
- **NOTION_KPI_DB_ID** – Notion database ID for KPI logging.
- **NOTION_DB_ID** – Notion database ID for uploading keyword metrics.
- **KEYWORD_OUTPUT_PATH** – path to save keyword data (default: `data/keyword_output_with_cpc.json`).
- **HOOK_OUTPUT_PATH** – path to save generated hooks (default: `data/generated_hooks.json`).
- **FAILED_HOOK_PATH** – path to store hooks that failed to generate (default: `logs/failed_hooks.json`).
- **REPARSED_OUTPUT_PATH** – path for reparsed failed keywords (default: `logs/failed_keywords_reparsed.json`).
- **UPLOAD_DELAY** – delay between uploads in seconds.
- **RETRY_DELAY** – delay between retries in seconds.
- **API_DELAY** – delay between OpenAI API calls in seconds.
- **UPLOADED_CACHE_PATH** – cache file for uploaded keywords (default: `data/uploaded_keywords_cache.json`).
- **FAILED_UPLOADS_PATH** – path for failed keyword uploads (default: `logs/failed_uploads.json`).
- **TOPIC_CHANNELS_PATH** – path to topic configuration (default: `config/topic_channels.json`).
- **SLACK_WEBHOOK_URL** – Slack webhook for workflow notifications (used in GitHub Actions).

## Running the Pipeline

### Manual Execution

Run the full pipeline locally using the top-level script:

```bash
python run_pipeline.py
```

This will execute the individual steps in order:

1. Generate hooks using `hook_generator.py`.
2. Parse and retry failed items.
3. Upload results to Notion.
4. Update dashboard metrics.

### GitHub Actions

The repository contains a workflow file at `.github/workflows/daily-pipeline.yml.txt` which runs the pipeline on a schedule. Configure the required secrets in the repository settings and enable the workflow.

You can also trigger it manually from the Actions tab using the `workflow_dispatch` event.

