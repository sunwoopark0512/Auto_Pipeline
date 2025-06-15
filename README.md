# Auto_Pipeline

**Project Goals**

The repository automates the discovery of trending keywords, generation of marketing hooks and uploading of the results to Notion. The scripts use Google Trends, Twitter metrics and OpenAI GPT models to build content ideas that can later be referenced by marketing teams.

**Pipeline Overview**

1. `keyword_auto_pipeline.py` collects candidate keywords using Google Trends and Twitter. The filtered results are stored in `data/keyword_output_with_cpc.json`.
2. `hook_generator.py` uses OpenAI GPT to generate hook lines, blog paragraphs and video titles for each keyword.
3. `notion_hook_uploader.py` uploads the generated hooks to the configured Notion database.
4. `retry_failed_uploads.py` attempts to re-upload any entries that previously failed.
5. `retry_dashboard_notifier.py` updates KPI information for retries in another Notion database.
6. `run_pipeline.py` orchestrates these steps sequentially.

**Script Usage**

Each script can be executed directly with `python <script_name>`. Environment variables are loaded from a local `.env` file. When running the full pipeline you can simply execute:

```bash
python run_pipeline.py
```

Some scripts inside the `scripts/` directory (`notion_uploader.py`, `retry_failed_uploads.py`) can also be invoked individually when needed.

**Environment Variables**

The pipeline expects several variables to be present:

- `OPENAI_API_KEY` – API key for OpenAI GPT models
- `NOTION_API_TOKEN` – token for the Notion API
- `NOTION_DB_ID` – ID of the Notion database for keyword upload
- `NOTION_HOOK_DB_ID` – ID of the Notion database for generated hooks
- `NOTION_KPI_DB_ID` – ID of the Notion database where KPI stats are stored
- `KEYWORD_OUTPUT_PATH` – path where keyword data is saved (default `data/keyword_output_with_cpc.json`)
- `HOOK_OUTPUT_PATH` – path for generated hooks JSON (default `data/generated_hooks.json`)
- `FAILED_HOOK_PATH` – location to save failed hook generations (default `logs/failed_hooks.json`)
- `FAILED_UPLOADS_PATH` – path for failed Notion uploads (default `logs/failed_uploads.json`)
- `REPARSED_OUTPUT_PATH` – file used by retry scripts to track unresolved uploads
- `UPLOAD_DELAY` – delay between Notion upload requests
- `UPLOADED_CACHE_PATH` – cache file to prevent duplicate uploads
- `API_DELAY` – delay between OpenAI API calls
- `RETRY_DELAY` – delay between retry attempts
- `TOPIC_CHANNELS_PATH` – configuration file for topics

**Example `.env` Template**

```env
OPENAI_API_KEY=
NOTION_API_TOKEN=
NOTION_DB_ID=
NOTION_HOOK_DB_ID=
NOTION_KPI_DB_ID=
SLACK_WEBHOOK_URL=
KEYWORD_OUTPUT_PATH=data/keyword_output_with_cpc.json
HOOK_OUTPUT_PATH=data/generated_hooks.json
FAILED_HOOK_PATH=logs/failed_hooks.json
FAILED_UPLOADS_PATH=logs/failed_uploads.json
REPARSED_OUTPUT_PATH=logs/failed_keywords_reparsed.json
UPLOAD_DELAY=0.5
UPLOADED_CACHE_PATH=data/uploaded_keywords_cache.json
API_DELAY=1.0
RETRY_DELAY=0.5
TOPIC_CHANNELS_PATH=config/topic_channels.json
```

**GitHub Actions Workflow**

The repository contains `.github/workflows/daily-pipeline.yml.txt` which schedules the pipeline to run daily and also allows manual execution. The workflow checks out the code, installs dependencies, and runs the pipeline using:

```yaml
- name: ▶️ Run full pipeline (single entrypoint)
  run: python scripts/run_pipeline.py
```

Failed keywords are uploaded as artifacts and a short summary is appended to the workflow run page.
