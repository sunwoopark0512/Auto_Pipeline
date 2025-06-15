# Auto Pipeline

This project collects trending keywords, generates marketing hooks using GPT, and uploads the results to Notion. The repository contains a series of standalone scripts that can be chained together with `run_pipeline.py`.

## Required Environment Variables
Set the following variables (typically via a `.env` file) before running the scripts:

- `OPENAI_API_KEY` – API key for OpenAI (used by `hook_generator.py`).
- `NOTION_API_TOKEN` – token for accessing the Notion API.
- `NOTION_DB_ID` – database ID for uploading raw keyword metrics (`scripts/notion_uploader.py`).
- `NOTION_HOOK_DB_ID` – database ID for storing generated hooks (`notion_hook_uploader.py` and retry scripts).
- `NOTION_KPI_DB_ID` – KPI database for dashboard notifications (`retry_dashboard_notifier.py`).
- `TOPIC_CHANNELS_PATH` – path to `topic_channels.json` used by `keyword_auto_pipeline.py`. Defaults to `config/topic_channels.json`.
- `KEYWORD_OUTPUT_PATH` – JSON output of collected keyword metrics. Defaults to `data/keyword_output_with_cpc.json`.
- `HOOK_OUTPUT_PATH` – JSON file of generated hooks. Defaults to `data/generated_hooks.json`.
- `FAILED_HOOK_PATH` – JSON file where failed generations are stored. Defaults to `logs/failed_hooks.json`.
- `REPARSED_OUTPUT_PATH` – parsed retry log path for retry scripts. Defaults to `logs/failed_keywords_reparsed.json`.
- `UPLOAD_DELAY`, `RETRY_DELAY`, and `API_DELAY` – optional delays between API calls.
- Additional paths such as `UPLOADED_CACHE_PATH` and `FAILED_UPLOADS_PATH` are used by `scripts/notion_uploader.py`.

## Setup
1. Install Python 3.10 or later.
2. Install dependencies:
   ```bash
   pip install openai notion-client pytrends snscrape-python python-dotenv
   ```
3. Create a `.env` file in the project root and define the environment variables listed above.
4. Ensure the `config/topic_channels.json` file exists or provide a custom path via `TOPIC_CHANNELS_PATH`.

## Running the Pipeline
Execute the full process using:
```bash
python run_pipeline.py
```
This command sequentially runs the helper scripts defined in `run_pipeline.py`.

Individual scripts can also be run separately if needed:
- `keyword_auto_pipeline.py` – collects trending keywords from Google Trends and Twitter and writes the results to `KEYWORD_OUTPUT_PATH`.
- `hook_generator.py` – reads the keyword JSON and generates marketing hooks with GPT, saving to `HOOK_OUTPUT_PATH` and `FAILED_HOOK_PATH`.
- `notion_hook_uploader.py` – uploads generated hooks to the Notion database specified by `NOTION_HOOK_DB_ID`.
- `retry_failed_uploads.py` – attempts to re-upload failed hooks stored in `REPARSED_OUTPUT_PATH`.
- `retry_dashboard_notifier.py` – summarizes retry statistics and records them in the KPI database.
- `scripts/notion_uploader.py` – optional script for uploading raw keyword metrics to a different Notion database.
- `scripts/retry_failed_uploads.py` – legacy variant of the retry uploader working with `FAILED_HOOK_PATH`.

## Expected Data Paths
- `config/topic_channels.json` – channel and topic definitions used for keyword collection.
- `data/keyword_output_with_cpc.json` – default location for collected keyword metrics.
- `data/generated_hooks.json` – storage for generated hook text.
- `logs/failed_hooks.json` and `logs/failed_keywords_reparsed.json` – logging of failures for later retries.

These directories are created automatically when running the scripts.
