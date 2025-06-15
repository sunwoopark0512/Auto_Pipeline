# Auto Pipeline

This repository automates the flow from keyword discovery to uploading marketing hooks to Notion.

## Workflow Overview

1. **Keyword Generation** (`keyword_auto_pipeline.py`)
   - Reads topics from `config/topic_channels.json`.
   - Collects data from Google Trends and Twitter to find high-scoring keywords.
   - Results are saved to `data/keyword_output_with_cpc.json`.

2. **Hook Creation** (`hook_generator.py`)
   - Uses the generated keywords to craft engaging hook phrases via GPT.
   - Outputs `data/generated_hooks.json` and logs failed attempts to `logs/failed_hooks.json`.

3. **Notion Upload** (`notion_hook_uploader.py`)
   - Uploads the generated hooks to a Notion database defined via environment variables.
   - Progress and errors are logged to `logs/notion_upload.log`.

`run_pipeline.py` orchestrates these steps in sequence and is the typical entry point for scheduled runs.

## Failure Handling & Retry Steps

- **Missing environment variables** will halt execution early. Ensure `.env` is populated with Notion and OpenAI credentials before running.
- **GPT errors or network timeouts** during hook creation create entries in `logs/failed_hooks.json`. Resolve API issues and re-run `hook_generator.py`.
- **Notion upload failures** produce `data/upload_failed_hooks.json`. Execute `retry_failed_uploads.py` or `scripts/retry_failed_uploads.py` to attempt another upload pass.
- Persistent upload issues should be investigated via `logs/notion_upload.log`. Check rate limits or database permissions.

## Logs and Monitoring

All major scripts write log files under the `logs/` directory. Inspect these files when diagnosing issues:

- `logs/notion_upload.log` – detailed upload log
- `logs/failed_hooks.json` – hooks that failed generation
- `logs/failed_keywords.json` / `logs/failed_keywords_reparsed.json` – upload failures and retry summaries

The GitHub Actions workflow in `.github/workflows/daily-pipeline.yml.txt` runs the pipeline daily and attaches failed items as artifacts for further inspection.

## Cleanup and Monitoring Scripts

- `retry_failed_uploads.py` and `scripts/retry_failed_uploads.py` retry previously failed uploads.
- `retry_dashboard_notifier.py` sends retry statistics to a Notion KPI database.
- `run_pipeline.py` can be executed manually to run all stages in order and check console output for quick monitoring.

