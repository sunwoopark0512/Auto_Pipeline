# Auto Pipeline

This project automates keyword discovery, GPT hook generation and Notion uploads. The pipeline collects trending keywords, generates marketing hooks with ChatGPT and stores results in Notion databases. Failed uploads are retried and summarized daily.

## Environment variables

Set these variables in your environment or `.env` file before running the pipeline:

- `OPENAI_API_KEY` – API key for GPT calls
- `NOTION_API_TOKEN` – token for all Notion access
- `NOTION_HOOK_DB_ID` – Notion database ID for generated hooks
- `NOTION_KPI_DB_ID` – database ID for retry KPI logs
- `NOTION_DB_ID` – database ID for storing raw keywords
- `TOPIC_CHANNELS_PATH` – path to the topic list JSON
- `KEYWORD_OUTPUT_PATH` – where collected keyword JSON is written
- `HOOK_OUTPUT_PATH` – path to the generated hook file
- `FAILED_HOOK_PATH` – failed hook output location
- `REPARSED_OUTPUT_PATH` – path used for retry summaries
- `UPLOAD_DELAY` – delay between Notion uploads (seconds)
- `RETRY_DELAY` – delay between retry attempts
- `API_DELAY` – pause between GPT API requests
- `UPLOADED_CACHE_PATH` – path for uploaded keyword cache
- `FAILED_UPLOADS_PATH` – where failed keyword uploads are logged

## Usage

Install Python dependencies and run the pipeline:

```bash
pip install -r requirements.txt
python run_pipeline.py
```

The pipeline executes multiple scripts in sequence to produce hooks and upload them to Notion. Output JSON is stored under `data/` and log files under `logs/`.

## Automation

A GitHub Actions workflow (`.github/workflows/daily-pipeline.yml.txt`) runs the pipeline every day. Failed items are uploaded as artifacts and can be found in the `logs/` directory on the runner.
