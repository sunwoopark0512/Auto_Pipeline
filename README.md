# Auto Pipeline

This project contains a set of scripts that run sequentially to generate hook content and upload it to Notion.

## Pipeline Sequence

`run_pipeline.py` executes the following scripts in order:

1. **hook_generator.py** – generates hook text with GPT and saves the results.
2. **parse_failed_gpt.py** – parses any failed GPT results so they can be retried.
3. **retry_failed_uploads.py** – uploads the reparsed items to Notion.
4. **notify_retry_result.py** – sends a Slack notification summarising the retry outcome.
5. **retry_dashboard_notifier.py** – updates a KPI dashboard in Notion with the retry statistics.

Each script resides in the `scripts/` directory and can be run individually, but `run_pipeline.py` provides a single entry point.
