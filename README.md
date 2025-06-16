# Auto Pipeline

This repository contains scripts for generating keywords, retrieving social media trends, and uploading marketing hooks to Notion. Workflows are automated via GitHub Actions for daily execution.

## Setup

1. **Clone the repository** and install the required Python packages listed in `requirements.txt`.
2. **Create a `.env` file** in the project root. All API tokens and secret keys must be stored in this file and should never be committed to the repository.
3. **Run the pipeline** using `python run_pipeline.py` or via the provided GitHub Actions workflow.

## Security

- **Keep tokens in `.env`**: Do not store API keys directly in the source files. The `.gitignore` file already excludes `.env` and `logs/` to prevent accidental commits of secrets.
- **Create or rotate API keys** regularly: Generate new API keys through the corresponding provider's dashboard (OpenAI, Notion, Slack, etc.), update them in your `.env` file, and revoke old keys to reduce risk.
- **Avoid token output in logs**: Ensure that logging statements never print API tokens or secrets. Review log messages for sensitive information before sharing or uploading them.

