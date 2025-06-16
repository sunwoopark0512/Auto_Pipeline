# Auto_Pipeline

A collection of scripts for generating trending keywords, creating GPT hooks and uploading them to Notion. The entrypoint for the whole workflow is `run_pipeline.py` which runs several helper scripts in sequence.

## Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
2. **Prepare a `.env` file** in the project root with the required credentials.

## Environment Variables

The scripts use various environment variables. Common variables are listed below:

- `OPENAI_API_KEY` – API key for OpenAI.
- `NOTION_API_TOKEN` – token for the Notion API.
- `NOTION_DB_ID` – database ID where keywords are uploaded.
- `NOTION_HOOK_DB_ID` – database ID for storing generated hooks.
- `NOTION_KPI_DB_ID` – database ID used by the dashboard notifier.
- `HOOK_OUTPUT_PATH` – path to store generated hooks (default `data/generated_hooks.json`).
- `KEYWORD_OUTPUT_PATH` – path to save collected keywords (default `data/keyword_output_with_cpc.json`).
- `REPARSED_OUTPUT_PATH` – file containing failed items to retry (default `logs/failed_keywords_reparsed.json`).

Other variables such as `UPLOAD_DELAY`, `RETRY_DELAY` and `API_DELAY` can be set to control request pacing.

## Running the Pipeline

After installing requirements and creating the `.env` file, run:

```bash
python run_pipeline.py
```

This script sequentially executes each stage of the pipeline as defined in `run_pipeline.py`.
