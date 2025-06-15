# Auto Pipeline

This repository contains a small pipeline that fetches trending keywords, generates marketing hooks using GPT, and uploads the results to Notion.

## Scripts overview

- **keyword_auto_pipeline.py** – gathers trending keywords from Google Trends and Twitter, filters them by score and growth, and writes the results to `KEYWORD_OUTPUT_PATH`.
- **hook_generator.py** – reads the keywords JSON and calls OpenAI to create hook lines, blog paragraph drafts, and example video titles. Results are saved to `HOOK_OUTPUT_PATH` and failed entries are written to `FAILED_HOOK_PATH`.
- **notion_hook_uploader.py** – uploads generated hooks to a Notion database defined by `NOTION_HOOK_DB_ID`. Skips existing keywords and logs failures to `data/upload_failed_hooks.json`.
- **retry_failed_uploads.py** – attempts to upload entries stored in `REPARSED_OUTPUT_PATH` (typically the failed hooks file). Useful for re-running uploads after errors.
- **retry_dashboard_notifier.py** – summarizes retry results from `REPARSED_OUTPUT_PATH` and pushes KPI numbers to a Notion database specified by `NOTION_KPI_DB_ID`.

## Required environment variables

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | API key for OpenAI (used by `hook_generator.py`) |
| `NOTION_API_TOKEN` | Token for Notion API access |
| `NOTION_HOOK_DB_ID` | Database ID for storing generated hooks |
| `NOTION_KPI_DB_ID` | Database ID for storing retry statistics |
| `KEYWORD_OUTPUT_PATH` | Path for the keyword JSON file (default `data/keyword_output_with_cpc.json`) |
| `HOOK_OUTPUT_PATH` | Path for the generated hooks JSON (default `data/generated_hooks.json`) |
| `REPARSED_OUTPUT_PATH` | Path used to store failed or retried items (default `logs/failed_keywords_reparsed.json`) |
| `TOPIC_CHANNELS_PATH` | Path to topic configuration JSON (default `config/topic_channels.json`) |
| `FAILED_HOOK_PATH` | Location for failed GPT generations (default `logs/failed_hooks.json`) |
| `UPLOAD_DELAY` | Delay in seconds between Notion uploads (default `0.5`) |
| `RETRY_DELAY` | Delay in seconds between retry attempts (default `0.5`) |
| `API_DELAY` | Delay between OpenAI API calls (default `1.0`) |

## Running locally

1. Install dependencies (for example using `pip install -r requirements.txt`).
2. Set the required environment variables (see table above) or create a `.env` file.
3. Run the pipeline manually:

```bash
python keyword_auto_pipeline.py
python hook_generator.py
python notion_hook_uploader.py
python retry_failed_uploads.py
python retry_dashboard_notifier.py
```

`keyword_auto_pipeline.py` creates the initial keyword list and the subsequent scripts process and upload the data.

## Running with GitHub Actions

The repository includes a workflow `.github/workflows/daily-pipeline.yml.txt` that executes the pipeline on a schedule. The action sets the environment variables from repository secrets and runs `python scripts/run_pipeline.py`. Review the workflow file to adjust schedules or steps as needed.

