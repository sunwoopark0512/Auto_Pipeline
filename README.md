# Auto Pipeline

This project collects trending keywords, generates marketing hooks using GPT-4 and uploads the results to Notion.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file based on `.env.example` and fill in your API tokens and database IDs.
3. Run the pipeline:
   ```bash
   python run_pipeline.py
   ```

## Files
- `keyword_auto_pipeline.py` – collects keywords from Google Trends and Twitter.
- `hook_generator.py` – generates hook sentences and blog drafts via OpenAI.
- `notion_hook_uploader.py` – uploads generated hooks to Notion.
- `scripts/retry_failed_uploads.py` – retries failed uploads.
- `retry_dashboard_notifier.py` – writes retry statistics to Notion.

The workflow in `.github/workflows/daily-pipeline.yml.txt` runs the pipeline automatically each day via GitHub Actions.
