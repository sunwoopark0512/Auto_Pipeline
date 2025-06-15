# Auto Pipeline

This repository contains a set of scripts that collect trending keywords, generate marketing hooks with GPT, and upload the results to Notion. The pipeline also retries failed uploads and records KPI metrics.

## Environment Variables

Create a `.env` file in the project root or export the following variables in your shell before running the pipeline:

| Variable | Description |
| --- | --- |
| `OPENAI_API_KEY` | API key for OpenAI used in `hook_generator.py` |
| `NOTION_API_TOKEN` | Notion API token for all uploader scripts |
| `NOTION_DB_ID` | Notion database ID used by `scripts/notion_uploader.py` |
| `NOTION_HOOK_DB_ID` | Database ID for generated hooks |
| `NOTION_KPI_DB_ID` | Database ID for KPI summary updates |
| `TOP_RESULTS_LIMIT` | Number of top keywords to process (default behaviour depends on the scripts) |
| `MAX_WORKERS` | Concurrency level for threaded tasks such as keyword collection |
| `REPARSED_OUTPUT_PATH` | Path for retry summaries (used in retry scripts) |
| `UPLOAD_DELAY` | Delay between Notion uploads |
| `RETRY_DELAY` | Delay between retry attempts |

Additional variables like `KEYWORD_OUTPUT_PATH`, `HOOK_OUTPUT_PATH` and others can be used to customize file locations.

## Running the Pipeline

1. Install dependencies (requires a local `requirements.txt`):
   ```bash
   pip install -r requirements.txt
   ```
2. Run the main pipeline entrypoint:
   ```bash
   python run_pipeline.py
   ```
   This script executes keyword collection, hook generation, Notion uploads and retry steps in sequence.

## Tests and Linting

The project expects standard Python tooling. After installing development dependencies run:

```bash
pytest            # run unit tests
pylint **/*.py    # lint the codebase
```

Use your preferred virtual environment before executing the commands above.
