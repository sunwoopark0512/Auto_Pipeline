# Auto Pipeline

This project automates collecting trending keywords, generating marketing hooks with GPT, and uploading the results to Notion. A daily GitHub Actions workflow runs the pipeline automatically and stores logs.

## Pipeline Overview
1. **Keyword Collection** (`keyword_auto_pipeline.py`)
   - Reads topic channels from `TOPIC_CHANNELS_PATH` (defaults to `config/topic_channels.json`).
   - Fetches Google Trends and Twitter metrics, filtering promising keywords.
   - Writes results to `KEYWORD_OUTPUT_PATH` (default `data/keyword_output_with_cpc.json`).
2. **GPT Hook Generation** (`hook_generator.py`)
   - Uses `OPENAI_API_KEY` to call OpenAI and create hooks for each keyword.
   - Saves output to `HOOK_OUTPUT_PATH` (default `data/generated_hooks.json`).
   - Failed items are written to `FAILED_HOOK_PATH` (default `logs/failed_hooks.json`).
3. **Notion Upload** (`notion_hook_uploader.py`)
   - Uploads generated hooks to a Notion database identified by `NOTION_HOOK_DB_ID`.
   - Upload delays are controlled with `UPLOAD_DELAY` (seconds).
   - Failures remain in `FAILED_HOOK_PATH` for retries.
4. **Retry & KPI Dashboard**
   - `retry_failed_uploads.py` reads `REPARSED_OUTPUT_PATH` (default `logs/failed_keywords_reparsed.json`) and retries failed uploads with delay `RETRY_DELAY`.
   - `retry_dashboard_notifier.py` summarizes retry results and updates a KPI page in Notion via `NOTION_KPI_DB_ID`.

## Required Environment Variables
- `OPENAI_API_KEY`
- `NOTION_API_TOKEN`
- `NOTION_HOOK_DB_ID`
- `NOTION_KPI_DB_ID`
- `NOTION_DB_ID`
- `TOPIC_CHANNELS_PATH`
- `KEYWORD_OUTPUT_PATH`
- `HOOK_OUTPUT_PATH`
- `FAILED_HOOK_PATH`
- `REPARSED_OUTPUT_PATH`
- `UPLOAD_DELAY`
- `RETRY_DELAY`
- `API_DELAY`
- `UPLOADED_CACHE_PATH`
- `FAILED_UPLOADS_PATH`

## Usage
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the entire pipeline:
   ```bash
   python run_pipeline.py
   ```

Output JSON files are stored under the `data/` directory and logs under `logs/`.

## GitHub Actions Workflow
The workflow `.github/workflows/daily-pipeline.yml.txt` triggers daily. It installs dependencies, runs `python scripts/run_pipeline.py`, and uploads `logs/failed_keywords_reparsed.json` as an artifact. Workflow logs and artifacts are available in the GitHub Actions tab.
