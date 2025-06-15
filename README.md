# Auto Pipeline

This repository contains scripts for collecting trending keywords, generating marketing hooks using GPT, and uploading results to Notion. Environment variables are used to configure API credentials and file paths.

## Required Environment Variables

| Variable | Description |
| --- | --- |
| `OPENAI_API_KEY` | API key for OpenAI GPT access |
| `NOTION_API_TOKEN` | Notion integration token |
| `NOTION_HOOK_DB_ID` | ID of the Notion database for storing generated hooks |
| `NOTION_KPI_DB_ID` | ID of the Notion database for retry KPI logging |
| `NOTION_DB_ID` | ID of the Notion database for keyword uploads (scripts) |
| `KEYWORD_OUTPUT_PATH` | Path to store collected keyword JSON (default `data/keyword_output_with_cpc.json`) |
| `HOOK_OUTPUT_PATH` | Path for generated hook JSON (default `data/generated_hooks.json`) |
| `FAILED_HOOK_PATH` | Path for failed hook data (default `logs/failed_hooks.json`) |
| `UPLOAD_DELAY` | Delay between Notion uploads in seconds |
| `API_DELAY` | Delay between OpenAI API calls in seconds |
| `TOPIC_CHANNELS_PATH` | Path to topic configuration JSON |
| `REPARSED_OUTPUT_PATH` | Path for reparsed failed keywords |
| `RETRY_DELAY` | Delay between retry attempts |
| `UPLOADED_CACHE_PATH` | Cache file for already uploaded keywords |
| `FAILED_UPLOADS_PATH` | Path to failed keyword uploads |

## Running the Pipeline

1. Create a `.env` file and define all required environment variables.
2. Install dependencies (at minimum `pytest` for tests):
   ```bash
   pip install -r requirements.txt
   ```
3. Execute individual scripts or run the full pipeline:
   ```bash
   python hook_generator.py
   python notion_hook_uploader.py
   # or
   python run_pipeline.py
   ```

## Running Tests

Unit tests use `pytest` and can be executed with:

```bash
pytest
```

## Continuous Integration

GitHub Actions runs the tests on every push using `.github/workflows/test.yml`.
