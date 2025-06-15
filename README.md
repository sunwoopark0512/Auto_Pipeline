# Auto Pipeline

This repository contains a collection of utility scripts used to generate and upload
content to Notion. The main entry point is `run_pipeline.py` which sequentially
executes a list of scripts.

## Running the Pipeline

```bash
python run_pipeline.py
```

The runner searches for each script in both the repository root and the
`scripts/` directory, so you can keep helper utilities in either location.

## GitHub Workflow

The daily scheduled workflow in `.github/workflows/daily-pipeline.yml.txt`
invokes `python run_pipeline.py` to execute the full pipeline on GitHub
Actions.
