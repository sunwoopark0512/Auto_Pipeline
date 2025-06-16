# Auto Pipeline

This repository contains automation scripts for generating marketing hooks and uploading them to Notion databases. The project relies on several external APIs and requires a few environment variables to run.

## Setup

1. **Clone the repository** and create a Python virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Prepare environment variables**:
   - Copy `.env.example` to `.env`.
   - Fill in the API keys and other values in the new `.env` file.
4. **Run the pipeline**:
   ```bash
   python run_pipeline.py
   ```

## Security Reminders

- `.env` is excluded from version control via `.gitignore`. **Never commit your real secrets**.
- Rotate API keys on a regular basis and update the values in your `.env` file when you do.
- If you suspect that a key was committed accidentally, rotate it immediately and review the commit history and CI logs for exposure.

## Logs

Execution logs are saved under the `logs/` directory. Regularly review these logs to ensure that no sensitive information is written there by mistake.

