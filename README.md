# Auto Pipeline

This repository contains a collection of scripts used to generate keyword hooks and upload them to Notion. The pipeline is orchestrated through a single entrypoint script and is executed daily via GitHub Actions.

## Installation

```bash
bash scripts/install.sh
source .venv/bin/activate
```

## Configuration

Copy `.env.example` to `.env` and fill in your secrets.

## Running

```bash
python scripts/run_codex_pipeline.py
```

## CI

The workflow file resides in `.github/workflows/daily-pipeline.yml` and runs the pipeline on a schedule.

## License

This project is licensed under the MIT License.
