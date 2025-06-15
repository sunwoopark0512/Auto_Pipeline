# Notion Hook Pipeline

This repository generates trending marketing hooks and uploads them to Notion.

## Setup
1. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file defining required environment variables:
   - `OPENAI_API_KEY`
   - `NOTION_API_TOKEN`
   - `NOTION_HOOK_DB_ID`
   - `NOTION_KPI_DB_ID`
   - optional: `UPLOAD_DELAY`, `RETRY_DELAY`

## Usage
Run the full pipeline locally:
```bash
python run_pipeline.py
```

The GitHub Actions workflow runs daily and executes the same entrypoint.

