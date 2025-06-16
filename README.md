# Auto Pipeline

This project contains a set of scripts that automatically collect trending keywords, generate marketing hooks using OpenAI and upload the results to Notion. The typical workflow is:

1. **Keyword extraction** – `keyword_auto_pipeline.py` gathers data from Google Trends and Twitter and saves filtered keywords to a JSON file.
2. **Hook generation** – `hook_generator.py` reads the keyword JSON and calls OpenAI to generate hook lines, blog paragraphs and video title ideas. Results are written to a hooks JSON file.
3. **Uploading to Notion** – `notion_hook_uploader.py` uploads the generated hooks to your Notion database. Additional retry scripts are provided to handle failed uploads.
4. **Pipeline runner** – `run_pipeline.py` can be used to execute the full sequence of scripts at once.

## Environment Variables
All scripts rely on environment variables. Create a `.env` file (see `.env.example`) containing the following keys:

- `OPENAI_API_KEY` – API key used by OpenAI.
- `KEYWORD_OUTPUT_PATH` – path where `keyword_auto_pipeline.py` stores keywords.
- `HOOK_OUTPUT_PATH` – path where generated hooks are saved.
- `FAILED_HOOK_PATH` – output path for failed hook generation items.
- `TOPIC_CHANNELS_PATH` – path to the JSON file describing topic to channel mappings.
- `API_DELAY` – delay in seconds between OpenAI API calls.
- `NOTION_API_TOKEN` – token for authenticating requests to Notion.
- `NOTION_DB_ID` – Notion database ID used by `scripts/notion_uploader.py`.
- `NOTION_HOOK_DB_ID` – Notion database ID used to store generated hooks.
- `NOTION_KPI_DB_ID` – database ID used for dashboard statistics.
- `UPLOAD_DELAY` – delay in seconds between Notion upload requests.
- `UPLOADED_CACHE_PATH` – cache file path for uploaded keywords.
- `FAILED_UPLOADS_PATH` – path for logging failed keyword uploads.
- `REPARSED_OUTPUT_PATH` – file used by retry scripts to store/parse failed items.
- `RETRY_DELAY` – delay between retry attempts.

## Example Usage
```bash
# 1. Collect trending keywords
python keyword_auto_pipeline.py

# 2. Generate hook sentences from the keywords
python hook_generator.py

# 3. Upload generated hooks to Notion
python notion_hook_uploader.py

# Optionally run the entire sequence
python run_pipeline.py
```

Ensure that all required environment variables are configured before running any script.
