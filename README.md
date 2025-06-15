# Auto Pipeline

This repository automates generation of marketing hooks and uploads them to Notion.

## Project Goals
- Collect trending keywords from Google Trends and Twitter.
- Generate marketing hook sentences, blog paragraphs and video titles using OpenAI GPT.
- Upload the generated content to specific Notion databases.
- Retry uploads that failed and track key performance metrics.

## Pipeline Steps
1. **keyword_auto_pipeline.py** – gathers trending keywords and saves them to `data/keyword_output_with_cpc.json`.
2. **hook_generator.py** – uses GPT to produce hook lines and draft text for each keyword.
3. **notion_hook_uploader.py** – uploads generated hooks to your Notion database.
4. **retry_failed_uploads.py** / **scripts/retry_failed_uploads.py** – attempts to upload items that previously failed.
5. **retry_dashboard_notifier.py** – summarises retry results and updates a KPI table in Notion.
6. **run_pipeline.py** – orchestrates the above steps in sequence. The GitHub Actions workflow runs `python scripts/run_pipeline.py`.

## Running Locally
1. Copy `.env.example` to `.env` and fill in your API keys and database IDs.
2. Install dependencies: `pip install -r requirements.txt`.
3. Execute individual scripts or run `python run_pipeline.py` to process the full pipeline.

## GitHub Actions
The workflow file at `.github/workflows/daily-pipeline.yml.txt` triggers the pipeline every day via a cron schedule and can also be run manually. It sets environment secrets and executes the `scripts/run_pipeline.py` entry point.

