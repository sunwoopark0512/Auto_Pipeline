# Auto Pipeline

This repository contains automation scripts used for generating and uploading Notion hooks. The main entry point is `run_pipeline.py` which sequentially executes several helper scripts.

## Running Locally

```bash
python run_pipeline.py
```

`run_pipeline.py` automatically looks for each pipeline script both in the repository root and in the `scripts/` directory so you can place your scripts in either location.

## GitHub Actions

The daily pipeline workflow executes `run_pipeline.py` directly. See `.github/workflows/daily-pipeline.yml.txt` for details.
