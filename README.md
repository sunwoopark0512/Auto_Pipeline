# Auto Pipeline

This repository contains utilities to generate marketing hooks and upload them to Notion. All executable scripts now reside in the `scripts/` directory. The main entry point is `scripts/run_pipeline.py` which coordinates the other scripts in order.

## Usage

```bash
python scripts/run_pipeline.py
```

The GitHub Actions workflow also calls this script to run the daily pipeline.

