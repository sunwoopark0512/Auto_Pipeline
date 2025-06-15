# Auto Pipeline

This repository contains a set of scripts that generate marketing hooks from trending keywords and uploads them to Notion.  The workflow can be run locally or via GitHub Actions.

## Pipeline Overview

1. **`keyword_auto_pipeline.py`** – Collects trending keywords from Google Trends and Twitter, applying thresholds for popularity and growth.  The output is stored in `data/keyword_output_with_cpc.json` by default.
2. **`hook_generator.py`** – Reads the keyword JSON, uses OpenAI GPT to create hook sentences, blog paragraphs and video title ideas, then saves results to `data/generated_hooks.json`.
3. **`notion_hook_uploader.py`** – Uploads the generated hooks to a Notion database, ensuring each keyword is only uploaded once.
4. **`retry_failed_uploads.py`** – Attempts to re-upload any hooks that previously failed to upload.
5. **`retry_dashboard_notifier.py`** – Summarises retry statistics and pushes them to a KPI database in Notion.
6. **`run_pipeline.py`** – Runs the above scripts in sequence. Additional helper utilities live under the `scripts/` directory.

## Environment Variables

Create a `.env` file at the project root and provide the following variables:

```
OPENAI_API_KEY=your-openai-key
NOTION_API_TOKEN=your-notion-token
NOTION_HOOK_DB_ID=your-hook-database-id
NOTION_KPI_DB_ID=your-kpi-database-id
NOTION_DB_ID=your-keyword-database-id           # used by scripts/notion_uploader.py
TOPIC_CHANNELS_PATH=config/topic_channels.json  # optional, path to topics json
KEYWORD_OUTPUT_PATH=data/keyword_output_with_cpc.json
HOOK_OUTPUT_PATH=data/generated_hooks.json
FAILED_HOOK_PATH=logs/failed_hooks.json
REPARSED_OUTPUT_PATH=logs/failed_keywords_reparsed.json
UPLOADED_CACHE_PATH=data/uploaded_keywords_cache.json
FAILED_UPLOADS_PATH=logs/failed_uploads.json
API_DELAY=1.0
UPLOAD_DELAY=0.5
RETRY_DELAY=0.5
```

These match the variables read in each script, e.g. `OPENAI_API_KEY` and paths in `hook_generator.py`【F:hook_generator.py†L10-L16】 and the Notion credentials in `notion_hook_uploader.py`【F:notion_hook_uploader.py†L11-L16】.

## Running Locally

1. Install Python 3.10+ and dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Populate the `.env` file with the variables above.
3. Run the keyword pipeline:
   ```bash
   python keyword_auto_pipeline.py
   python hook_generator.py
   python notion_hook_uploader.py
   ```
   The helper `run_pipeline.py` can execute multiple retry scripts sequentially.

## GitHub Actions

The repository includes a workflow file `.github/workflows/daily-pipeline.yml.txt`.  It runs every day and on manual trigger.  The job sets required secrets (`OPENAI_API_KEY`, `NOTION_API_TOKEN`, etc.), installs dependencies and runs `scripts/run_pipeline.py` before uploading any failure logs. Key steps are shown below:

```
name: Daily Notion Hook Pipeline
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
    NOTION_API_TOKEN: ${{ secrets.NOTION_API_TOKEN }}
    NOTION_HOOK_DB_ID: ${{ secrets.NOTION_HOOK_DB_ID }}
    NOTION_KPI_DB_ID: ${{ secrets.NOTION_KPI_DB_ID }}
  steps:
    - name: 🛠️ Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: ▶️ Run full pipeline (single entrypoint)
      run: python scripts/run_pipeline.py
```

Failed keywords are saved as workflow artifacts and a short summary is appended to the run log.【F:.github/workflows/daily-pipeline.yml.txt†L10-L49】
