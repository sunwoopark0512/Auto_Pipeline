# Auto Pipeline

This project contains a set of Python scripts that generate trending keywords, create marketing hooks using GPT, and upload results to Notion. The scripts can be composed into an end-to-end pipeline using `run_pipeline.py`.

## Setup

1. Install Python 3.10 or later.
2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in the required tokens and database IDs.

## Scripts

| Script | Description | Required Environment Variables |
|-------|-------------|--------------------------------|
| `keyword_auto_pipeline.py` | Collects trending keywords from Google Trends and Twitter, filters them, and saves results to a JSON file. | `TOPIC_CHANNELS_PATH` (path to `topic_channels.json`), `KEYWORD_OUTPUT_PATH` (output JSON file) |
| `hook_generator.py` | Uses GPT to generate hook sentences, blog drafts, and video titles for each keyword. | `OPENAI_API_KEY`, `KEYWORD_OUTPUT_PATH`, `HOOK_OUTPUT_PATH`, `FAILED_HOOK_PATH`, `API_DELAY` |
| `notion_hook_uploader.py` | Uploads generated hooks to a Notion database. | `NOTION_API_TOKEN`, `NOTION_HOOK_DB_ID`, `HOOK_OUTPUT_PATH`, `UPLOAD_DELAY` |
| `scripts/notion_uploader.py` | Uploads filtered keywords directly to a Notion database. | `NOTION_API_TOKEN`, `NOTION_DB_ID`, `KEYWORD_OUTPUT_PATH`, `UPLOAD_DELAY`, `UPLOADED_CACHE_PATH`, `FAILED_UPLOADS_PATH` |
| `retry_failed_uploads.py` | Retries failed hook uploads recorded in `logs/failed_keywords_reparsed.json`. | `NOTION_API_TOKEN`, `NOTION_HOOK_DB_ID`, `REPARSED_OUTPUT_PATH`, `RETRY_DELAY` |
| `retry_dashboard_notifier.py` | Publishes KPI statistics about retry results to a Notion dashboard. | `NOTION_API_TOKEN`, `NOTION_KPI_DB_ID`, `REPARSED_OUTPUT_PATH` |
| `run_pipeline.py` | Executes the pipeline sequence defined in `PIPELINE_SEQUENCE`. | None |

### Example Usage

Running each step individually:
```bash
python keyword_auto_pipeline.py      # generate keywords
python hook_generator.py             # create hooks with GPT
python notion_hook_uploader.py       # upload hooks to Notion
```

Running the entire pipeline:
```bash
python run_pipeline.py
```

## Dependency Installation

The project relies on the packages listed in `requirements.txt`:
```text
openai
python-dotenv
notion-client
pytrends
snscrape
```
Install them using `pip install -r requirements.txt`.

## Full Pipeline Execution

1. Configure environment variables in `.env`.
2. Run `python keyword_auto_pipeline.py` to gather keywords.
3. Run `python hook_generator.py` to generate marketing hooks.
4. Run `python notion_hook_uploader.py` to push hooks to Notion.
5. Optionally, execute `python retry_failed_uploads.py` and `python retry_dashboard_notifier.py` to handle any failed uploads and log KPIs.
6. For convenience, run `python run_pipeline.py` to execute the entire sequence.

## Future Integration

*Supabase tracking*: Future versions will log keyword and hook generation metrics into a Supabase table for centralized analytics.

*GPT refinement loops*: The hook generation step can be extended to trigger additional GPT passes that refine content based on performance metrics stored in Supabase.

