# Auto Pipeline

This repository provides a Python pipeline for collecting trending keywords, generating marketing hooks using OpenAI, and uploading the results to Notion. The scripts can be run locally or scheduled in CI.

## Requirements
- Python 3.10+
- `pip install -r requirements.txt`
- A `.env` file with the environment variables below

## Environment Variables
Create a `.env` file in the project root with the following values (sample):

```
OPENAI_API_KEY=sk-...
NOTION_API_TOKEN=secret_...
NOTION_HOOK_DB_ID=your_hook_db_id
NOTION_DB_ID=your_keyword_db_id
NOTION_KPI_DB_ID=your_kpi_db_id
KEYWORD_OUTPUT_PATH=data/keyword_output_with_cpc.json
HOOK_OUTPUT_PATH=data/generated_hooks.json
FAILED_HOOK_PATH=logs/failed_hooks.json
REPARSED_OUTPUT_PATH=logs/failed_keywords_reparsed.json
TOPIC_CHANNELS_PATH=config/topic_channels.json
UPLOADED_CACHE_PATH=data/uploaded_keywords_cache.json
FAILED_UPLOADS_PATH=logs/failed_uploads.json
UPLOAD_DELAY=0.5
API_DELAY=1.0
RETRY_DELAY=0.5
```

## Running the Pipeline
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Populate `.env` with the values above.
3. Execute the pipeline:
   ```bash
   python run_pipeline.py
   ```
   The entry script will run each stage located in the `scripts/` directory.

## Project Structure
- `keyword_auto_pipeline.py` – fetches trending keywords from Google Trends and Twitter
- `hook_generator.py` – generates marketing hooks using OpenAI
- `notion_hook_uploader.py` – uploads generated hooks to Notion
- `scripts/` – helper utilities used by the main pipeline

Logs and intermediate files are stored in the `logs/` and `data/` folders.
