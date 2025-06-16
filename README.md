# Auto Pipeline

This repository contains a collection of scripts for generating trending keywords, creating marketing hooks with OpenAI, and uploading the results to Notion databases. The code can be run locally or automated via GitHub Actions.

## Required Environment Variables
Set the following variables in your environment or in an `.env` file before running any scripts:

| Variable | Description |
| --- | --- |
| `OPENAI_API_KEY` | API key for OpenAI GPT models. |
| `NOTION_API_TOKEN` | Integration token for the Notion API. |
| `NOTION_DB_ID` | Notion database ID used by `scripts/notion_uploader.py`. |
| `NOTION_HOOK_DB_ID` | Notion database ID used for storing generated hooks. |
| `NOTION_KPI_DB_ID` | Notion database ID used by `retry_dashboard_notifier.py`. |
| `KEYWORD_OUTPUT_PATH` | Path for keyword JSON output. Defaults to `data/keyword_output_with_cpc.json`. |
| `HOOK_OUTPUT_PATH` | Path for generated hook JSON output. Defaults to `data/generated_hooks.json`. |
| `FAILED_HOOK_PATH` | Path where failed hook generation results are stored. |
| `UPLOAD_DELAY` | Delay (in seconds) between Notion uploads. |
| `UPLOADED_CACHE_PATH` | Cache file for uploaded keywords. |
| `FAILED_UPLOADS_PATH` | File containing failed uploads. |
| `REPARSED_OUTPUT_PATH` | Input file for retry operations. |
| `RETRY_DELAY` | Delay (in seconds) between retry attempts. |
| `TOPIC_CHANNELS_PATH` | Path to `config/topic_channels.json`. |
| `API_DELAY` | Delay (in seconds) between OpenAI API calls. |

## Pipeline Steps
1. **Keyword collection** – `keyword_auto_pipeline.py` gathers trending keywords from Google Trends and Twitter.
2. **Hook generation** – `hook_generator.py` uses GPT to create marketing hooks for each keyword.
3. **Upload to Notion** – `notion_hook_uploader.py` (or `scripts/notion_uploader.py`) uploads generated hooks to the configured Notion database.
4. **Retry failures** – `retry_failed_uploads.py` attempts to re-upload any failed items.
5. **Dashboard update** – `retry_dashboard_notifier.py` summarizes retry results in a KPI database.
6. The `run_pipeline.py` script can execute multiple steps in sequence.

## Running Locally
1. Install dependencies: `pip install -r requirements.txt` (requires internet access).
2. Set the environment variables above.
3. Execute individual scripts directly, for example:
   ```bash
   python keyword_auto_pipeline.py
   python hook_generator.py
   python notion_hook_uploader.py
   ```
4. Alternatively, run the full pipeline:
   ```bash
   python run_pipeline.py
   ```

## Running with GitHub Actions
Create a workflow in `.github/workflows/` that checks out the repository, installs dependencies, sets the environment variables (via repository secrets), and executes `python run_pipeline.py`. This allows the pipeline to run automatically on a schedule or in response to events.

## Policy and Algorithm Compliance
The repository uses open-source libraries for data collection (Google Trends, Twitter scraping) and Notion integration. It also relies on the OpenAI API for text generation. All code is intended for lawful use and follows the platform's policies regarding safe content generation and data handling. The algorithms implemented follow standard public methods and do not include proprietary or malicious logic.

