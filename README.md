# Auto Pipeline

This repository contains a collection of small Python utilities that work together to collect trending keywords, generate marketing hooks using OpenAI, and upload the results to Notion databases.  Each script can be run individually, or you can execute the full pipeline through the provided GitHub Actions workflow.

## Installing Dependencies

Use `pip` to install the required packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Required Environment Variables

The scripts rely on the following environment variables.  You can place them in a `.env` file or export them before running a script.

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI API key used by `hook_generator.py` |
| `NOTION_API_TOKEN` | Token for the Notion API |
| `NOTION_DB_ID` | Database ID for keyword uploads (`scripts/notion_uploader.py`) |
| `NOTION_HOOK_DB_ID` | Database ID for generated hooks |
| `NOTION_KPI_DB_ID` | Database ID for KPI metrics |
| `KEYWORD_OUTPUT_PATH` | Path to save keyword JSON results |
| `HOOK_OUTPUT_PATH` | Path for generated hook output |
| `FAILED_HOOK_PATH` | Log path for failed hook generation |
| `UPLOAD_DELAY` | Delay (seconds) between Notion uploads |
| `API_DELAY` | Delay (seconds) between OpenAI API calls |
| `TOPIC_CHANNELS_PATH` | Location of `config/topic_channels.json` |
| `REPARSED_OUTPUT_PATH` | Path used by retry scripts for failed items |
| `RETRY_DELAY` | Delay between retry attempts |
| `UPLOADED_CACHE_PATH` | Cache path for successful uploads |
| `FAILED_UPLOADS_PATH` | Log path for failed keyword uploads |

## Running the Scripts

- **`keyword_auto_pipeline.py`** – Collects trending keywords from Google Trends and Twitter and writes them to `KEYWORD_OUTPUT_PATH`.
- **`hook_generator.py`** – Uses the keywords to generate hooks through the OpenAI API and saves them to `HOOK_OUTPUT_PATH`.
- **`notion_hook_uploader.py`** – Uploads generated hooks to the Notion database specified by `NOTION_HOOK_DB_ID`.
- **`scripts/notion_uploader.py`** – Uploads raw keyword metrics to the Notion database specified by `NOTION_DB_ID`.
- **`retry_failed_uploads.py`** and **`scripts/retry_failed_uploads.py`** – Retry uploading failed items stored at `REPARSED_OUTPUT_PATH` or `FAILED_HOOK_PATH`.
- **`retry_dashboard_notifier.py`** – Updates KPI statistics in Notion using results from the retry step.
- **`run_pipeline.py`** – Runs the individual scripts in order. Each step is executed from the `scripts` directory.

Run any script with Python 3.10 or later:

```bash
python <script_name>.py
```

## GitHub Actions Workflow

The `.github/workflows/daily-pipeline.yml.txt` file defines a workflow that installs dependencies, runs `python scripts/run_pipeline.py`, and uploads any failed items as an artifact.  The workflow is scheduled to run daily and also supports manual execution through the **Run workflow** button in the Actions tab.

To trigger the workflow manually:

1. Push your changes to GitHub.
2. Navigate to the **Actions** tab of your repository.
3. Select **Daily Notion Hook Pipeline** and choose **Run workflow**.

