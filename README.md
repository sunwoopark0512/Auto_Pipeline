# Auto Pipeline

This repository automates the generation of marketing hooks from trending keywords and uploads them to Notion. The code is organized as a set of standalone scripts that can be executed individually or through a central pipeline runner.

## Pipeline Overview

1. **Keyword collection** – `keyword_auto_pipeline.py`
   - Fetches trending keywords from Google Trends and Twitter.
   - Stores results in `data/keyword_output_with_cpc.json` (controlled by `KEYWORD_OUTPUT_PATH`).
2. **Hook generation** – `hook_generator.py`
   - Uses the OpenAI API to create hook sentences, blog draft paragraphs and YouTube titles for each keyword.
   - Outputs `data/generated_hooks.json` (`HOOK_OUTPUT_PATH`).
3. **Upload to Notion** – `notion_hook_uploader.py`
   - Uploads generated hooks to the Notion database specified by `NOTION_HOOK_DB_ID`.
4. **Retry failed uploads** – `retry_failed_uploads.py`
   - Attempts to re‑upload hooks recorded in `logs/failed_keywords_reparsed.json` (`REPARSED_OUTPUT_PATH`).
5. **Dashboard update** – `retry_dashboard_notifier.py`
   - Summarizes retry statistics and pushes KPI information to a separate Notion database (`NOTION_KPI_DB_ID`).
6. **Pipeline runner** – `run_pipeline.py`
   - Runs the above scripts sequentially. The default sequence is defined by `PIPELINE_SEQUENCE`.

Additional scripts in `scripts/` provide utilities such as uploading raw keyword metrics to another Notion database.

## Running Scripts Manually

Each script can be executed with Python after preparing a `.env` file with the required variables:

```bash
python keyword_auto_pipeline.py
python hook_generator.py
python notion_hook_uploader.py
python retry_failed_uploads.py
python retry_dashboard_notifier.py
python run_pipeline.py
```

## Environment Variables

Create a `.env` file (see `.env.example`) with your API tokens, database IDs and optional paths. The major variables include `OPENAI_API_KEY`, `NOTION_API_TOKEN`, and `NOTION_HOOK_DB_ID`.

## GitHub Actions

The workflow file [`daily-pipeline.yml.txt`](.github/workflows/daily-pipeline.yml.txt) runs the full pipeline on a schedule. It checks out the repository, installs dependencies, and executes `python scripts/run_pipeline.py`. Failed keywords are uploaded as artifacts for inspection and a summary is appended to the workflow output.

