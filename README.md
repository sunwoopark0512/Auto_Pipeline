# Auto Pipeline

This repository contains scripts for generating keyword hooks from social data and uploading the results to Notion.

## Installation

1. Ensure you have Python 3.10 installed.
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Configure environment variables as needed (see scripts for details) and run the pipeline script:

```bash
python run_pipeline.py
```

The GitHub Actions workflow also installs packages from `requirements.txt` when running automatically.
