# Notion Hook Auto Pipeline

This project collects trending keywords, generates marketing hooks using OpenAI, and uploads the results to Notion. Failed uploads are retried and summarized for dashboard tracking.

## Pipeline Stages
1. **Keyword Collection** – `keyword_auto_pipeline.py` gathers keywords from Google Trends and Twitter, filters them and saves them to `KEYWORD_OUTPUT_PATH`.
2. **Hook Generation** – `hook_generator.py` reads the collected keywords and uses OpenAI to generate short-form hooks, blog drafts and video titles. The results are stored in `HOOK_OUTPUT_PATH`.
3. **Notion Upload** – `notion_hook_uploader.py` uploads the generated hooks to a Notion database defined by `NOTION_HOOK_DB_ID`.
4. **Retry & KPI Update** – `retry_failed_uploads.py` retries failed uploads using data from `REPARSED_OUTPUT_PATH`. `retry_dashboard_notifier.py` posts success metrics to a KPI database.

`run_pipeline.py` can be used to execute these stages in sequence.

## Environment Variables
| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | API key for OpenAI used when generating hooks. |
| `NOTION_API_TOKEN` | Token for accessing the Notion API. |
| `NOTION_HOOK_DB_ID` | Notion database ID where hooks are uploaded. |
| `NOTION_KPI_DB_ID` | Notion database ID for retry statistics. |
| `KEYWORD_OUTPUT_PATH` | File path for keyword JSON output. |
| `HOOK_OUTPUT_PATH` | File path for generated hook JSON. |
| `REPARSED_OUTPUT_PATH` | File path for items that failed to upload and need retrying. |
| `TOPIC_CHANNELS_PATH` | *(optional)* Path to topic/channel configuration. |
| `FAILED_HOOK_PATH` | *(optional)* Path to store failed hook generations. |
| `UPLOAD_DELAY` | *(optional)* Delay between Notion upload requests. |
| `API_DELAY` | *(optional)* Delay between OpenAI API requests. |
| `RETRY_DELAY` | *(optional)* Delay between retry attempts. |

## Running Locally
1. Install Python 3.10 and dependencies (see `requirements.txt` if present):
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file or export the environment variables listed above.
3. Run the full pipeline:
   ```bash
   python run_pipeline.py
   ```
   Individual stages can be executed by running their respective scripts.

## Running with GitHub Actions
The repository includes a workflow definition at `.github/workflows/daily-pipeline.yml.txt` which runs the pipeline on a schedule. It expects the same environment variables to be provided as GitHub Secrets:

```yaml
    env:
      OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      NOTION_API_TOKEN: ${{ secrets.NOTION_API_TOKEN }}
      NOTION_HOOK_DB_ID: ${{ secrets.NOTION_HOOK_DB_ID }}
      NOTION_KPI_DB_ID: ${{ secrets.NOTION_KPI_DB_ID }}
```

To enable the workflow, rename the file to `daily-pipeline.yml` and push to GitHub. The job installs dependencies and calls `python scripts/run_pipeline.py` to execute the pipeline.
