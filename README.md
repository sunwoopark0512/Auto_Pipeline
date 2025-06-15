# Auto Pipeline

This project automates the collection of trending keywords, generates marketing hooks with GPT, and uploads the results to Notion. The pipeline can be executed manually or scheduled through GitHub Actions.

## Environment Variables

The scripts rely on the following variables. They can be placed in a `.env` file or exported in your environment.

- `OPENAI_API_KEY` – OpenAI API key used by `hook_generator.py`.
- `NOTION_API_TOKEN` – Token for Notion API access.
- `NOTION_DB_ID` – Notion database ID for keyword metrics (used by `scripts/notion_uploader.py`).
- `NOTION_HOOK_DB_ID` – Database ID for generated hooks.
- `NOTION_KPI_DB_ID` – Database ID for retry statistics.
- `KEYWORD_OUTPUT_PATH` – Path for the keyword output JSON (default `data/keyword_output_with_cpc.json`).
- `HOOK_OUTPUT_PATH` – Path for generated hook data (default `data/generated_hooks.json`).
- `TOPIC_CHANNELS_PATH` – Input topic list JSON (default `config/topic_channels.json`).
- `UPLOADED_CACHE_PATH` – Cache for successfully uploaded keywords.
- `FAILED_UPLOADS_PATH` – File for keywords that failed to upload.
- `FAILED_HOOK_PATH` – File where failed hook generations are stored.
- `REPARSED_OUTPUT_PATH` – File for items that failed and were reprocessed.
- `API_DELAY` – Delay between OpenAI requests.
- `UPLOAD_DELAY` – Delay between Notion uploads.
- `RETRY_DELAY` – Delay used during retry operations.

## Running Locally

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure your environment variables (for example create a `.env` file).
3. Execute the full pipeline:
   ```bash
   python run_pipeline.py
   ```
   Individual steps can also be run directly (e.g. `python keyword_auto_pipeline.py`).

## GitHub Actions

The repository includes a workflow at `.github/workflows/daily-pipeline.yml.txt` that runs the pipeline on a schedule or when manually triggered. Secrets for the environment variables above must be configured in your repository settings. The workflow installs dependencies from `requirements.txt` and then runs `python scripts/run_pipeline.py`.

