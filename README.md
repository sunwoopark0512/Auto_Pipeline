# Auto Pipeline

This repository provides a small pipeline that discovers trending keywords, generates marketing hooks via GPT, and uploads the results to Notion. The scripts are meant to run together but can also be executed individually.

## Workflow Overview

1. **`keyword_auto_pipeline.py`** collects potential keywords from Google Trends and Twitter, filtering them by score and CPC before saving to `KEYWORD_OUTPUT_PATH`.
2. **`hook_generator.py`** uses the filtered keywords and the OpenAI API to produce hook sentences, blog drafts and video title ideas.
3. **`notion_hook_uploader.py`** uploads generated hooks to a Notion database.
4. **`retry_failed_uploads.py`** retries uploading hooks that previously failed.
5. **`retry_dashboard_notifier.py`** sends KPI summaries of the retries to a Notion dashboard.
6. **`run_pipeline.py`** provides a simple wrapper to run the above steps in sequence.

## Environment Variables

The scripts rely on several environment variables which can be placed in a `.env` file:

- `OPENAI_API_KEY` – API key used by `hook_generator.py` to call the OpenAI API.
- `NOTION_API_TOKEN` – authentication token for all Notion uploads.
- `NOTION_HOOK_DB_ID` – target database where generated hooks are stored.
- `NOTION_KPI_DB_ID` – Notion database for retry statistics (used by `retry_dashboard_notifier.py`).
- `NOTION_DB_ID` – database for uploading raw keywords (`scripts/notion_uploader.py`).
- `TOPIC_CHANNELS_PATH` – JSON file that lists default topics for keyword discovery.
- `KEYWORD_OUTPUT_PATH` – location of the keyword output JSON (read by multiple scripts).
- `HOOK_OUTPUT_PATH` – file path for generated hooks.
- `FAILED_HOOK_PATH` – path to store hooks that could not be generated.
- `UPLOADED_CACHE_PATH` – cache file for already uploaded keywords.
- `FAILED_UPLOADS_PATH` – log path for keyword uploads that failed.
- `REPARSED_OUTPUT_PATH` – file holding hooks that failed to upload and were parsed again.
- `UPLOAD_DELAY` – delay between Notion uploads in seconds.
- `API_DELAY` – delay between OpenAI API requests.
- `RETRY_DELAY` – delay when retrying failed uploads.
- `SLACK_WEBHOOK_URL` – optional Slack webhook used in the GitHub workflow.

## Usage

1. Install dependencies (Python 3.10 or higher):

```bash
pip install -r requirements.txt  # install libraries such as openai, notion-client, pytrends, snscrape
```

2. Create a `.env` file containing the necessary environment variables shown above.

3. Run the individual steps manually if desired:

```bash
python keyword_auto_pipeline.py       # generate `keyword_output_with_cpc.json`
python hook_generator.py              # create hooks from the keywords
python notion_hook_uploader.py        # upload generated hooks to Notion
python retry_failed_uploads.py        # retry any failed uploads
python retry_dashboard_notifier.py    # push retry KPI stats
```

Alternatively, run the entire pipeline with:

```bash
python run_pipeline.py
```

The scheduled GitHub Action in `.github/workflows/daily-pipeline.yml.txt` provides an example of running the pipeline daily.
