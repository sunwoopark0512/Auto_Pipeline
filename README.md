# Auto_Pipeline

This repository contains automation scripts for generating marketing hooks, uploading data to Notion, and retry workflows.

## Setup

Install Python 3.10 and the project dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the full pipeline locally:

```bash
python scripts/run_pipeline.py
```

The CI workflow also installs dependencies from `requirements.txt` before executing the pipeline.
