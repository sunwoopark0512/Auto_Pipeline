# Auto Pipeline

Auto Pipeline automates finding trending keywords, generating marketing hooks using GPT, and uploading results to Notion.

## Pipeline Overview

1. **keyword_auto_pipeline.py** – Collects trending keywords from Google Trends and Twitter and saves them to `data/keyword_output_with_cpc.json`.
2. **hook_generator.py** – Uses OpenAI GPT to create two hook sentences, a short blog draft, and YouTube title ideas for each keyword.
3. **notion_hook_uploader.py** – Uploads the generated hooks to a Notion database.
4. **retry_failed_uploads.py** – Attempts to re-upload any failed items.
5. **retry_dashboard_notifier.py** – Summarises retry results and records them to a KPI dashboard in Notion.
6. **run_pipeline.py** – Runs the above scripts sequentially.

## Environment Variables

Create a `.env` file in the project root and provide the following variables:

```
OPENAI_API_KEY=your_openai_key
NOTION_API_TOKEN=your_notion_integration_token
NOTION_DB_ID=your_keyword_database_id
NOTION_HOOK_DB_ID=your_hook_database_id
NOTION_KPI_DB_ID=your_kpi_database_id
```

Optional variables can override default paths and delays:

```
KEYWORD_OUTPUT_PATH=data/keyword_output_with_cpc.json
HOOK_OUTPUT_PATH=data/generated_hooks.json
FAILED_HOOK_PATH=logs/failed_hooks.json
UPLOAD_DELAY=0.5
API_DELAY=1.0
RETRY_DELAY=0.5
UPLOADED_CACHE_PATH=data/uploaded_keywords_cache.json
FAILED_UPLOADS_PATH=logs/failed_uploads.json
REPARSED_OUTPUT_PATH=logs/failed_keywords_reparsed.json
TOPIC_CHANNELS_PATH=config/topic_channels.json
```

## Usage

Install dependencies (for example with `pip`):

```bash
pip install openai notion-client python-dotenv pytrends snscrape
```

Run individual scripts:

```bash
python keyword_auto_pipeline.py            # fetch trending keywords
python hook_generator.py                   # generate hooks with GPT
python notion_hook_uploader.py             # upload hooks to Notion
python retry_failed_uploads.py             # retry failed uploads
python retry_dashboard_notifier.py         # update KPI dashboard
```

Run the entire pipeline:

```bash
python run_pipeline.py
```

