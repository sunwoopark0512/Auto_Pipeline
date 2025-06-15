# Auto Pipeline

This repository contains a collection of scripts for generating marketing content and synchronising data with Notion.

## Pipeline Execution

The `run_pipeline.py` orchestrates a sequence of scripts located in the `scripts/` directory.
The current pipeline order is:

1. `hook_generator.py` – generates marketing hooks using GPT.
2. `retry_failed_uploads.py` – retries uploading failed hooks to Notion.
3. `retry_dashboard_notifier.py` – updates KPI dashboards in Notion.

Run the pipeline with:

```bash
python run_pipeline.py
```
