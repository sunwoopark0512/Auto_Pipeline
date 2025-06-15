# Auto Pipeline

This repository contains scripts used to generate marketing hooks from keywords and upload them to Notion.  A small pipeline orchestrates several steps.

## Pipeline Stages

1. **hook_generator.py** – Generates hook text using GPT.
2. **parse_failed_gpt.py** – Parses raw GPT output from failed items for later retries.
3. **retry_failed_uploads.py** – Attempts to upload the reparsed keywords again.
4. **notify_retry_result.py** – Sends a Slack notification summarizing retry results.
5. **retry_dashboard_notifier.py** – Updates KPI metrics in Notion.

Run `python run_pipeline.py` to execute these steps sequentially.
