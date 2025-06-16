# Auto Pipeline

This repository contains Python scripts that generate keyword hooks using OpenAI and upload them to Notion. A GitHub Actions workflow (`daily-pipeline.yml.txt`) runs the pipeline on a schedule.

## Setup

1. Install Python 3.10 or higher.
2. Clone this repository and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root and define the required environment variables.
4. Run the pipeline locally with:
   ```bash
   python run_pipeline.py
   ```

### Environment variables

The scripts read configuration values from environment variables using `python-dotenv`. Important variables include:

- `OPENAI_API_KEY`
- `NOTION_API_TOKEN`
- `NOTION_HOOK_DB_ID`
- `NOTION_KPI_DB_ID`
- `SLACK_WEBHOOK_URL`
- other optional variables such as `KEYWORD_OUTPUT_PATH`, `HOOK_OUTPUT_PATH` and retry delays.

Refer to the GitHub Actions workflow for a full list of variables.

## Managing Secrets

Sensitive values (API keys, tokens, database IDs) must be stored in the `.env` file **which is ignored by Git** (see `.gitignore`). Never commit this file to the repository. Regularly rotate API keys and monitor their usage. Delete and recreate any key that is suspected of being compromised.

