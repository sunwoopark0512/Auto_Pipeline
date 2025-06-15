# Auto Pipeline

This project generates trending marketing hooks and uploads them to Notion. It collects trending keywords from Google Trends and Twitter, generates content using OpenAI, and stores or uploads the results. A GitHub Actions workflow can run the pipeline daily.

## Environment Variables

Create a `.env` file based on `.env.example` and provide the following variables:

- `OPENAI_API_KEY` – API key for OpenAI GPT.
- `NOTION_API_TOKEN` – Integration token for the Notion API.
- `NOTION_HOOK_DB_ID` – Notion database ID that stores generated hooks.
- `NOTION_KPI_DB_ID` – Notion database ID used by `retry_dashboard_notifier.py`.
- `NOTION_DB_ID` – Database for storing raw keyword metrics.
- `TOPIC_CHANNELS_PATH` – Path to the JSON configuration of topics (default `config/topic_channels.json`).
- `KEYWORD_OUTPUT_PATH` – Where keyword results are saved (default `data/keyword_output_with_cpc.json`).
- `HOOK_OUTPUT_PATH` – File to write generated hooks (default `data/generated_hooks.json`).
- `FAILED_HOOK_PATH` – Path for failed hook generation logs (default `logs/failed_hooks.json`).
- `REPARSED_OUTPUT_PATH` – File for storing failed keyword reparse results (default `logs/failed_keywords_reparsed.json`).
- `UPLOADED_CACHE_PATH` – Cache file of uploaded keywords.
- `FAILED_UPLOADS_PATH` – Log file for failed keyword uploads.
- `API_DELAY` – Seconds to wait between OpenAI API calls.
- `UPLOAD_DELAY` – Delay between Notion uploads.
- `RETRY_DELAY` – Delay between retry attempts.
- `SLACK_WEBHOOK_URL` – Optional Slack webhook for GitHub Actions notifications.

## Local Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and fill in the variables.
3. Run the pipeline:
   ```bash
   python run_pipeline.py
   ```
   Individual scripts such as `keyword_auto_pipeline.py` or `notion_hook_uploader.py` can also be executed separately.

## GitHub Actions

The workflow file [`daily-pipeline.yml.txt`](.github/workflows/daily-pipeline.yml.txt) runs the pipeline on a schedule. Configure repository secrets for the variables listed above so the job can access the OpenAI and Notion APIs. Once set up, the pipeline will automatically run according to the cron schedule or when triggered manually.
