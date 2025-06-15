# Auto Pipeline

This project automates keyword collection, hook generation with OpenAI, and uploading results to Notion. It is intended to run both locally and in GitHub Actions.

## Environment Variables

Create a `.env` file or set the following variables in your environment:

- `OPENAI_API_KEY` – API key for OpenAI
- `NOTION_API_TOKEN` – Notion integration token
- `NOTION_HOOK_DB_ID` – Notion database ID for generated hooks
- `NOTION_KPI_DB_ID` – Notion database ID for KPI logging
- `NOTION_DB_ID` – Notion database ID used when uploading keywords
- `KEYWORD_OUTPUT_PATH` – Path for collected keyword JSON
- `HOOK_OUTPUT_PATH` – Path for generated hook JSON
- `FAILED_HOOK_PATH` – Path to store hooks that failed to upload
- `REPARSED_OUTPUT_PATH` – File used when retrying failed uploads
- `UPLOADED_CACHE_PATH` – Cache file for uploaded keywords
- `FAILED_UPLOADS_PATH` – Path to log keyword uploads that failed
- `TOPIC_CHANNELS_PATH` – JSON configuration of topics
- `API_DELAY` – Delay between OpenAI API calls
- `UPLOAD_DELAY` – Delay between Notion upload requests
- `RETRY_DELAY` – Delay when retrying failed uploads

See `.env.example` for an example file.

## Local Execution

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create your `.env` file with the variables above.
3. Run individual scripts such as:

```bash
python keyword_auto_pipeline.py
python hook_generator.py
python notion_hook_uploader.py
```

`run_pipeline.py` executes the entire sequence.

## GitHub Actions

The repository contains a workflow (`.github/workflows/daily-pipeline.yml.txt`) that runs the pipeline daily. Secrets for the required environment variables must be configured in your GitHub repository for the workflow to succeed.
