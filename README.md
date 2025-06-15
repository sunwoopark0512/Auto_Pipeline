# Auto Pipeline

This project automates the generation of trending keywords, creates engaging hooks using OpenAI and uploads the results to Notion. It is designed to run either locally or on GitHub Actions.

## Environment Variables

Set the following environment variables (e.g. in a `.env` file):

- `OPENAI_API_KEY` – API key for OpenAI.
- `NOTION_API_TOKEN` – token for the Notion API.
- `NOTION_HOOK_DB_ID` – Notion database where generated hooks are stored.
- `NOTION_DB_ID` – database for storing keyword metrics.
- `NOTION_KPI_DB_ID` – database for KPI tracking.
- Optional paths such as `KEYWORD_OUTPUT_PATH`, `HOOK_OUTPUT_PATH`, `FAILED_HOOK_PATH` etc. have defaults defined in the code.

## Quick Start

1. Install the required Python packages (`openai`, `notion-client`, `python-dotenv`, `pytrends`, `snscrape`, etc.).
2. Generate trending keywords:

   ```bash
   python keyword_auto_pipeline.py
   ```

   This creates `data/keyword_output_with_cpc.json`.
3. Generate hooks from those keywords:

   ```bash
   python hook_generator.py
   ```

   The results are saved to `data/generated_hooks.json`.
4. Run the entire pipeline:

   ```bash
   python run_pipeline.py
   ```

   This executes the scripts listed in `run_pipeline.py` sequentially.

## GitHub Actions

A workflow file is available at `.github/workflows/daily-pipeline.yml.txt`. After pushing the repository to GitHub you can run this workflow from the **Actions** tab or wait for the scheduled daily run.
