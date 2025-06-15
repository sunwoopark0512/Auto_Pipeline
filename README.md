# Auto Pipeline

This repository contains scripts for generating and uploading hooks to Notion as part of an automated pipeline.

The main entrypoint for running the full workflow is `run_pipeline.py`. The GitHub Actions workflow calls this script directly.

## Missing scripts

The original pipeline referenced `parse_failed_gpt.py` and `notify_retry_result.py`, but these files are not included in the repository. The pipeline definition in `run_pipeline.py` has been updated to comment out these entries.
