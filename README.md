# Auto Pipeline

This repo contains scripts for generating marketing hooks and uploading them to Notion.

## Environment Variables

- `NOTION_API_TOKEN` – API token for Notion access
- `NOTION_HOOK_DB_ID` – target Notion database for hooks
- `REPARSED_OUTPUT_PATH` – path to the JSON file containing reparsed failed items (default: `logs/failed_keywords_reparsed.json`)
- `RETRY_DELAY` – delay in seconds between retry attempts

## Running the pipeline

All pipeline steps are orchestrated via `scripts/run_pipeline.py`:

```bash
python scripts/run_pipeline.py
```

The GitHub Actions workflow also calls this script.
