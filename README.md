# Auto Pipeline

This repository contains a collection of scripts that generate hooks and upload them to Notion. The daily workflow executes `run_pipeline.py` which sequentially runs each script listed in `PIPELINE_SEQUENCE`.

## Setup

1. Copy `.env.example` to `.env` and fill in your credentials.
2. Run `scripts/install.sh` to install dependencies.
3. Execute the pipeline locally with `python run_pipeline.py` or rely on the GitHub Actions workflow which runs daily.

## Testing

Run `pytest` to execute the smoke tests.
