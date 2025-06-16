# Auto Pipeline

This repository contains scripts for automatically generating hooks and uploading trending keywords to Notion.

## Setup/Security

1. **Environment Variables**: Secrets such as API tokens should be stored in a `.env` file at the project root. The scripts load this file using `python-dotenv`.
2. **Avoid Committing Credentials**: Never commit your `.env` file or any credentials to the repository. The `.gitignore` already ignores `.env`, so ensure it stays that way.
3. **Rotate and Monitor Tokens**: Rotate API keys regularly. Check your logs for any accidental token output and remove or regenerate the keys if this occurs.

