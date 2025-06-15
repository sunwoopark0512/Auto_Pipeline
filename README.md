# Auto Pipeline

This repository contains scripts for generating marketing hooks and uploading them to Notion.
It automates keyword collection, hook generation via OpenAI, and Notion updates.

## Setup

1. Install **Python 3.10** or later.
2. Install dependencies:
   ```bash
   pip install openai python-dotenv notion-client pytrends snscrape
   ```
   Alternatively, use `requirements.txt` if available.
3. Copy `.env.example` to `.env` and fill in values.

## Usage

Run the main pipeline:

```bash
python run_pipeline.py
```

Each step logs progress and saves JSON results under the `data/` and `logs/` folders.

## Environment Variables

Key settings are loaded from `.env`:

- `OPENAI_API_KEY` – OpenAI API key
- `NOTION_API_TOKEN` – Notion integration token
- `NOTION_DB_ID` – Notion database for keywords
- `NOTION_HOOK_DB_ID` – Notion database for generated hooks
- `NOTION_KPI_DB_ID` – Notion KPI database
- `KEYWORD_OUTPUT_PATH` – path for collected keywords JSON
- `HOOK_OUTPUT_PATH` – path for generated hooks JSON
- `FAILED_HOOK_PATH` – path for failed hooks JSON
- `FAILED_UPLOADS_PATH` – path for failed uploads JSON
- `UPLOADED_CACHE_PATH` – path for upload cache JSON
- `REPARSED_OUTPUT_PATH` – path for retried keywords JSON
- `TOPIC_CHANNELS_PATH` – topic configuration file
- `API_DELAY` – delay between OpenAI API calls (seconds)
- `UPLOAD_DELAY` – delay between Notion uploads (seconds)
- `RETRY_DELAY` – delay before retrying failed uploads (seconds)
- `TOP_RESULTS_LIMIT` – maximum number of results processed per topic

Adjust these paths and limits as needed.
