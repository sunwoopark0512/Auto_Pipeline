# Auto_Pipeline

This repository contains scripts used to generate marketing hooks with GPT and upload results to Notion.

## Pipeline Steps

The pipeline is executed via `run_pipeline.py` and runs scripts from the `scripts/` directory in the following order:

1. `hook_generator.py` – generate hooks with GPT.
2. `parse_failed_gpt.py` – parse failed GPT outputs for retry.
3. `retry_failed_uploads.py` – upload parsed failures again.
4. `notify_retry_result.py` – print a summary of retry results.
5. `retry_dashboard_notifier.py` – push KPI data to Notion.

Run the pipeline:

```bash
python run_pipeline.py
```

Unit tests are located in the `tests/` folder and can be run with:

```bash
python -m unittest discover -s tests -v
```
