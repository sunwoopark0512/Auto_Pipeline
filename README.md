# Auto Pipeline

This repository provides scripts for gathering trending keywords, generating marketing hooks, and uploading the results to Notion.

## Environment Variables

The scripts read settings from the environment (or a `.env` file). Key variables include:

- `OPENAI_API_KEY` – API key for OpenAI used by `hook_generator.py`.
- `NOTION_API_TOKEN` – token for the Notion API.
- `NOTION_DB_ID` – database ID for the keyword upload script.
- `NOTION_HOOK_DB_ID` – database ID where generated hooks are stored.
- `NOTION_KPI_DB_ID` – database ID for retry statistics.
- `TOPIC_CHANNELS_PATH` – path to `topic_channels.json` used by `keyword_auto_pipeline.py`.
- `KEYWORD_OUTPUT_PATH` – path where the keyword collector writes results.
- `HOOK_OUTPUT_PATH` – path where generated hooks are saved.
- `REPARSED_OUTPUT_PATH` – path for the cleaned failed keyword list.

Refer to each script for additional optional variables such as `UPLOAD_DELAY` and `API_DELAY`.

## Basic Usage

1. **Collect trending keywords**
   ```bash
   python keyword_auto_pipeline.py
   ```
   Generates a JSON file at `KEYWORD_OUTPUT_PATH` with filtered keywords.

2. **Generate hooks using GPT**
   ```bash
   python hook_generator.py
   ```
   Reads the keyword file and writes hook content to `HOOK_OUTPUT_PATH`.

3. **Run the full pipeline**
   ```bash
   python run_pipeline.py
   ```
   Executes the helper scripts in sequence to upload results and process failures.

## Scheduled Runs

A GitHub Actions workflow (`.github/workflows/daily-pipeline.yml.txt`) is configured to run the pipeline automatically every day at midnight UTC (9 AM KST):

```yaml
on:
  schedule:
    - cron: '0 0 * * *'
```

Use the workflow file as a reference if you wish to enable automated runs in your fork.
