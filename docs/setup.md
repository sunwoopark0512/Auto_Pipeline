# Environment Setup

1. **Python**: Install Python 3.10 or higher.
2. **Virtual Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install openai notion-client python-dotenv pytrends snscrape
   ```
4. **Environment Variables**: Create a `.env` file with the following keys:
   - `OPENAI_API_KEY`
   - `NOTION_API_TOKEN`
   - `NOTION_HOOK_DB_ID`
   - `NOTION_KPI_DB_ID` (optional)
   - `NOTION_DB_ID` (optional)
   - `REPARSED_OUTPUT_PATH` (defaults to `logs/failed_keywords_reparsed.json`)
   - `UPLOAD_DELAY` (defaults to `0.5`)
   - `RETRY_DELAY` (defaults to `0.5`)
   - `API_DELAY` (defaults to `1.0`)

See other scripts for additional optional paths such as `KEYWORD_OUTPUT_PATH` and `HOOK_OUTPUT_PATH`.
