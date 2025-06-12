# Auto Pipeline

This repository contains a collection of Python scripts used to generate hook text from keywords and upload the results to Notion. The pipeline is executed via `run_pipeline.py` and consists of the following steps:

1. `hook_generator.py` – generates hook sentences using GPT and stores them.
2. `retry_failed_uploads.py` – retries any uploads that previously failed.
3. `retry_dashboard_notifier.py` – updates the KPI dashboard in Notion.

Earlier versions referenced `parse_failed_gpt.py` and `notify_retry_result.py`, but these scripts are no longer part of the process.

## Running locally

Install the required dependencies and execute the pipeline:

```bash
python run_pipeline.py
```
