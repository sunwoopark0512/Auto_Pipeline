# Auto Pipeline

This repository contains a collection of Python scripts used to gather trending keywords, generate marketing hooks with OpenAI, and upload the results to Notion. A GitHub Actions workflow is included to run the full pipeline on a schedule.

## Scripts

| Script | Purpose | Required Environment Variables |
| ------ | ------- | ------------------------------ |
| `keyword_auto_pipeline.py` | Collect trending keywords from Google Trends and Twitter, then save filtered results to `data/keyword_output_with_cpc.json`. | `TOPIC_CHANNELS_PATH` (optional path to `config/topic_channels.json`), `KEYWORD_OUTPUT_PATH` |
| `hook_generator.py` | Use OpenAI to generate hook sentences, blog draft and video titles for each keyword. | `OPENAI_API_KEY`, `KEYWORD_OUTPUT_PATH`, `HOOK_OUTPUT_PATH`, `FAILED_HOOK_PATH`, `API_DELAY` |
| `notion_hook_uploader.py` | Upload generated hooks to a Notion database. | `NOTION_API_TOKEN`, `NOTION_HOOK_DB_ID`, `HOOK_OUTPUT_PATH`, `UPLOAD_DELAY` |
| `retry_failed_uploads.py` | Retry uploading hooks that previously failed (`logs/failed_keywords_reparsed.json`). | `NOTION_API_TOKEN`, `NOTION_HOOK_DB_ID`, `REPARSED_OUTPUT_PATH`, `RETRY_DELAY` |
| `retry_dashboard_notifier.py` | Push retry upload KPIs to another Notion database. | `NOTION_API_TOKEN`, `NOTION_KPI_DB_ID`, `REPARSED_OUTPUT_PATH` |
| `scripts/notion_uploader.py` | Upload filtered keywords to a Notion database. | `NOTION_API_TOKEN`, `NOTION_DB_ID`, `KEYWORD_OUTPUT_PATH`, `UPLOAD_DELAY`, `UPLOADED_CACHE_PATH`, `FAILED_UPLOADS_PATH` |
| `scripts/retry_failed_uploads.py` | Retry uploading hooks stored in `logs/failed_keywords.json`. | `NOTION_API_TOKEN`, `NOTION_HOOK_DB_ID`, `FAILED_HOOK_PATH`, `RETRY_DELAY` |
| `run_pipeline.py` | Orchestrate the pipeline by running the above scripts in sequence. | *(none)* |

## Installation

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Pipeline

Set up the necessary environment variables (see table above) in a `.env` file or your shell environment. Then execute:

```bash
python run_pipeline.py
```

The pipeline runs each step defined in `run_pipeline.py` and logs output under the `logs/` directory.

## GitHub Workflow

A GitHub Actions workflow is available in `.github/workflows/daily-pipeline.yml.txt`. To enable it, rename the file to `daily-pipeline.yml` and push it to your repository. The workflow installs dependencies, runs `python run_pipeline.py` daily, and uploads any failed keyword JSON as an artifact.
