# Auto Pipeline

This repository contains a collection of scripts that automate keyword discovery, content generation and upload flows.

## Project overview

1. **`keyword_auto_pipeline.py`** – collects trending keywords from Google Trends and Twitter.
2. **`hook_generator.py`** – generates marketing hooks for the keywords using OpenAI.
3. **`notion_hook_uploader.py`** – uploads generated hooks to a Notion database.
4. **`retry_failed_uploads.py`** – reattempts failed uploads.
5. **`retry_dashboard_notifier.py`** – pushes summary KPI data to a Notion dashboard.
6. **`run_pipeline.py`** – orchestrates the above steps.
7. **ROI analyzer** – analyzes the performance of uploaded hooks to evaluate return on investment.

## Required environment variables

Create a `.env` file in the project root with the following values (see individual scripts for defaults):

- `OPENAI_API_KEY` – API key for OpenAI requests.
- `NOTION_API_TOKEN` – token used to access the Notion APIs.
- `NOTION_DB_ID` – Notion database ID for keyword uploads.
- `NOTION_HOOK_DB_ID` – database ID where hooks are stored.
- `NOTION_KPI_DB_ID` – database for storing KPI statistics.
- `KEYWORD_OUTPUT_PATH` – path to save collected keywords.
- `HOOK_OUTPUT_PATH` – path to save generated hooks.
- `FAILED_HOOK_PATH` – path where failed hook generations are stored.
- `UPLOAD_DELAY` – delay between Notion uploads.
- `RETRY_DELAY` – delay when retrying failed uploads.
- `REPARSED_OUTPUT_PATH` – file used by retry scripts and dashboard notifier.

Additional environment variables may be used by optional tools such as the ROI analyzer.

## Running the pipeline

After installing the required dependencies (for example `pip install -r requirements.txt`), execute the pipeline from the project root:

```bash
python run_pipeline.py
```

Each stage logs its progress to the console. Generated files can be found under the `data/` and `logs/` directories.

## Using the ROI analyzer

The ROI analyzer evaluates how uploaded hooks perform. After running the main pipeline and accumulating results, run the analyzer:

```bash
python roi_analyzer.py
```

The analyzer reads your Notion metrics and prints a summary of ROI statistics. Adjust environment variables referenced in `roi_analyzer.py` to point to your metric exports.
