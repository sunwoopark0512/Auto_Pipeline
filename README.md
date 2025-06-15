# Auto Pipeline

This repository contains scripts for generating marketing hooks, retrying failed uploads, and notifying dashboards.

## Running the pipeline

Use the `run_pipeline.py` script located in the project root. It will automatically
look for scripts in the `scripts/` directory first and then fall back to
root-level scripts.

```bash
python run_pipeline.py
```

The GitHub workflow `.github/workflows/daily-pipeline.yml.txt` uses the same
entrypoint.
