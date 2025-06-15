# Auto Pipeline

This project collects trending keywords, generates marketing hooks using GPT, and uploads the results to Notion. The pipeline can be run locally or through the provided GitHub Actions workflow.

## Environment Variables
Create a `.env` file in the project root containing the following keys:

- `OPENAI_API_KEY` – API key for OpenAI.
- `NOTION_API_TOKEN` – token used to call the Notion API.
- `NOTION_HOOK_DB_ID` – ID of the Notion database where generated hooks are stored.
- `NOTION_KPI_DB_ID` – ID of the Notion database for retry KPI metrics.
- Optional paths such as `KEYWORD_OUTPUT_PATH`, `HOOK_OUTPUT_PATH`, `REPARSED_OUTPUT_PATH`, and delays like `API_DELAY`, `UPLOAD_DELAY`, `RETRY_DELAY` can be tweaked as needed.

## Running Locally
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Ensure the `.env` file is configured.
3. Execute the pipeline:
   ```bash
   python run_pipeline.py
   ```

The pipeline sequentially runs keyword collection, hook generation, upload to Notion and retry logic.

## GitHub Actions Workflow
The workflow definition resides in `.github/workflows/daily-pipeline.yml.txt`. It runs every day at midnight UTC (09:00 KST) and can also be triggered manually. The job installs Python 3.10, installs the dependencies with `pip install -r requirements.txt`, and runs `python scripts/run_pipeline.py`. Failed items are uploaded as an artifact and a summary is appended to the workflow output.
