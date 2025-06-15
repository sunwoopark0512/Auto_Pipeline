# Auto Pipeline

This repository contains a small set of scripts for generating marketing hooks and uploading them to Notion.  The pipeline is orchestrated by `run_pipeline.py` and executes a sequence of helper scripts located in `scripts/`.

## Pipeline Steps

1. **hook_generator.py** – Generates hook text for each keyword using GPT and saves both successful and failed results.
2. **parse_failed_gpt.py** – Parses the raw GPT output from `logs/failed_hooks.json` and stores a structured version in `logs/failed_keywords_reparsed.json`.
3. **retry_failed_uploads.py** – Attempts to upload any items that previously failed, using the parsed results.
4. **notify_retry_result.py** – Sends a short summary of the retry outcome to Slack (or prints the message if no webhook is configured).
5. **retry_dashboard_notifier.py** – Records aggregated retry statistics in a Notion KPI database.

Run the pipeline with:

```bash
python run_pipeline.py
```

Each script relies on environment variables for API tokens and paths. See the individual files for details.
