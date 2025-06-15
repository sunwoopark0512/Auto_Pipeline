# Auto Pipeline

This repository provides a small pipeline that collects trending keywords, generates marketing hooks with GPT, and uploads the result to Notion.  Each step can be executed separately or orchestrated in CI through GitHub Actions.

## Pipeline Overview

1. **Keyword collection** – `keyword_auto_pipeline.py`
   - Reads topics from `config/topic_channels.json` and scrapes Google Trends and Twitter metrics.
   - Filters the results and writes the output to `KEYWORD_OUTPUT_PATH`.
2. **Hook generation** – `hook_generator.py`
   - Uses the OpenAI API to craft hook sentences and other content for each keyword.
   - Saves the generated data to `HOOK_OUTPUT_PATH` and logs failures to `FAILED_HOOK_PATH`.
3. **Notion upload** – `notion_hook_uploader.py`
   - Uploads generated hooks to the Notion database specified by `NOTION_HOOK_DB_ID`.
   - Skips duplicates and records failed items for later retry.
4. **Retry steps** – `retry_failed_uploads.py` and `retry_dashboard_notifier.py`
   - `retry_failed_uploads.py` attempts to upload any hooks that previously failed.
   - `retry_dashboard_notifier.py` records retry statistics in a KPI database.

## Environment Variables

The following environment variables configure the pipeline. Defaults are shown for optional values.

| Variable | Description | Default |
| --- | --- | --- |
| `OPENAI_API_KEY` | API key for OpenAI used in hook generation. | – |
| `NOTION_API_TOKEN` | Notion API token. | – |
| `NOTION_HOOK_DB_ID` | Notion database ID where hooks are stored. | – |
| `NOTION_KPI_DB_ID` | Notion database ID for retry metrics. | – |
| `KEYWORD_OUTPUT_PATH` | Path to save collected keywords. | `data/keyword_output_with_cpc.json` |
| `HOOK_OUTPUT_PATH` | Path for generated hooks. | `data/generated_hooks.json` |
| `REPARSED_OUTPUT_PATH` | File used by retry scripts for failed items. | `logs/failed_keywords_reparsed.json` |
| `TOPIC_CHANNELS_PATH` | Topic configuration file for keyword collection. | `config/topic_channels.json` |
| `FAILED_HOOK_PATH` | Where to store failed hook generations. | `logs/failed_hooks.json` |
| `API_DELAY` | Delay between OpenAI API requests. | `1.0` |
| `UPLOAD_DELAY` | Delay between Notion uploads. | `0.5` |
| `RETRY_DELAY` | Delay between retry uploads. | `0.5` |

## Running Locally

Run each step in the listed order. Ensure all required environment variables are available in your shell or in a `.env` file.

```bash
python keyword_auto_pipeline.py
python hook_generator.py
python notion_hook_uploader.py
# Optional retry helpers
python retry_failed_uploads.py
python retry_dashboard_notifier.py
```

## GitHub Actions

The workflow file [`daily-pipeline.yml.txt`](.github/workflows/daily-pipeline.yml.txt) runs the pipeline on a schedule or on demand. It installs dependencies, loads secrets for the environment variables above and executes `scripts/run_pipeline.py`.

```yaml
- name: ▶️ Run full pipeline (single entrypoint)
  run: python scripts/run_pipeline.py
```

The workflow also uploads any failure logs as artifacts so they can be reviewed later.
