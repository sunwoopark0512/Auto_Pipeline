# Auto Pipeline

This repository contains scripts for generating trending keywords, creating marketing hooks, uploading content to Notion, and tracking failed uploads. The pipeline is designed to be run as a series of Python scripts.

## Environment Variables

Set these variables in a `.env` file or in your shell before running the pipeline:

- `OPENAI_API_KEY` – API key used by `hook_generator.py` for GPT requests.
- `NOTION_API_TOKEN` – authentication token for the Notion API.
- `NOTION_HOOK_DB_ID` – Notion database ID where generated hooks are stored.
- `NOTION_DB_ID` – Notion database ID used by `scripts/notion_uploader.py`.
- `NOTION_KPI_DB_ID` – database ID for storing KPI stats from `retry_dashboard_notifier.py`.
- `TOPIC_CHANNELS_PATH` – path to `topic_channels.json` (defaults to `config/topic_channels.json`).
- `KEYWORD_OUTPUT_PATH` – output path for keyword results (defaults to `data/keyword_output_with_cpc.json`).
- `HOOK_OUTPUT_PATH` – output path for generated hook data (defaults to `data/generated_hooks.json`).
- `FAILED_HOOK_PATH` – JSON file for storing failed hook generations.
- `UPLOAD_DELAY` – delay in seconds between Notion upload operations.
- `API_DELAY` – delay between OpenAI API calls when generating hooks.
- `UPLOADED_CACHE_PATH` – cache file used by `scripts/notion_uploader.py`.
- `FAILED_UPLOADS_PATH` – path where failed upload entries are written.
- `REPARSED_OUTPUT_PATH` – file containing reparsed keywords for retry scripts.
- `RETRY_DELAY` – delay in seconds between retry attempts.
- `SLACK_WEBHOOK_URL` – Slack webhook for workflow notifications (used in CI).
- `TOP_RESULTS_LIMIT` – number of top ranked keywords to keep. Increase or decrease this value to control how many results move on to later stages.

## Installation

1. Install Python 3.10 or higher.
2. Clone this repository and change into the project directory.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

(If `requirements.txt` is missing, install the packages referenced in the scripts: `openai`, `notion-client`, `python-dotenv`, `pytrends`, and `snscrape`.)

## Running the Pipeline

The entire pipeline can be executed from a single entry point:

```bash
python run_pipeline.py
```

This will run the sequence defined in `run_pipeline.py` which generates keywords, creates hook content using GPT, uploads data to Notion, and handles retries.

To run individual components manually you can execute each script directly, for example:

```bash
python keyword_auto_pipeline.py      # collect trending keywords
python hook_generator.py             # generate marketing hooks via GPT
python notion_hook_uploader.py       # upload hooks to Notion
```

### Adjusting `TOP_RESULTS_LIMIT`

`TOP_RESULTS_LIMIT` controls how many of the highest scoring keywords are kept after filtering. Set it as an environment variable before running the pipeline:

```bash
export TOP_RESULTS_LIMIT=20
python run_pipeline.py
```

Higher values produce a larger output set, while lower values speed up processing by limiting results.

## Tests and Linters

Run unit tests with `pytest`:

```bash
pytest
```

Code style and static checks can be executed with:

```bash
pylint *.py scripts/*.py
mypy *.py scripts/*.py
```

These commands help ensure consistent code quality across the project.
