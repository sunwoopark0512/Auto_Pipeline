# Auto Pipeline

This repository contains several Python scripts that collect trending keywords, generate marketing hooks using GPT, and upload the results to Notion. The scripts can be executed individually or through the main pipeline entrypoint.

## Required Environment Variables

The pipeline expects a `.env` file or environment variables with the following names:

- `OPENAI_API_KEY` – API key used by `hook_generator.py` to call OpenAI APIs.
- `NOTION_API_TOKEN` – Token for authenticating the Notion client.
- `NOTION_HOOK_DB_ID` – ID of the Notion database where generated hooks will be uploaded.
- `NOTION_DB_ID` – Target database for keyword metrics (used in `scripts/notion_uploader.py`).
- `NOTION_KPI_DB_ID` – Database for retry KPI metrics.

Optional variables control file locations and delays:

- `TOPIC_CHANNELS_PATH` – Path to `config/topic_channels.json` (defaults to that file).
- `KEYWORD_OUTPUT_PATH` – Output JSON file for collected keywords (default `data/keyword_output_with_cpc.json`).
- `HOOK_OUTPUT_PATH` – Output file for generated hooks (default `data/generated_hooks.json`).
- `FAILED_HOOK_PATH` – File for failed hook generations (default `logs/failed_hooks.json`).
- `UPLOAD_DELAY` – Delay (seconds) between uploads to Notion.
- `RETRY_DELAY` – Delay when retrying failed uploads.
- `API_DELAY` – Delay between OpenAI API calls.
- `REPARSED_OUTPUT_PATH` – Path for reparsed failed keyword data.

## Running the Pipeline

Install dependencies (Python 3.10 recommended) and then run the main entrypoint:

```bash
pip install -r requirements.txt  # install your own dependencies
python run_pipeline.py
```

`run_pipeline.py` executes several scripts in order:

1. `hook_generator.py` – reads keyword JSON and generates marketing hook text using GPT.
2. `parse_failed_gpt.py` – (optional) parse failed GPT outputs if present.
3. `retry_failed_uploads.py` – retries Notion uploads that previously failed.
4. `notify_retry_result.py` – (optional) notify about retry results.
5. `retry_dashboard_notifier.py` – updates KPI metrics in a Notion database.

Individual scripts can also be executed directly if needed.

## Linting and Tests

Run pylint to lint the code base and `pytest` for any tests:

```bash
pip install pylint pytest
pylint *.py scripts/*.py
pytest
```

The repository currently does not include test files, but `pytest` is recommended for any additions.
