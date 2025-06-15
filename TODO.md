# Additional Tasks for Auto_Pipeline

Below is a list of follow-up tasks that can enhance the current pipeline.

- [ ] **Implement missing scripts**: `parse_failed_gpt.py` and `notify_retry_result.py` referenced in `run_pipeline.py` are not present. Implement these modules to handle failed GPT results and retry notifications.
- [ ] **Add unit tests**: Create automated tests for all scripts to ensure correct behavior, especially around data parsing and Notion API interactions.
- [ ] **Update CI workflow**: Extend `.github/workflows/daily-pipeline.yml.txt` or create a new workflow to run tests and linters on each commit.
- [ ] **Provide documentation**: Add a README with setup instructions, environment variables, and pipeline usage details.
- [ ] **Improve error handling**: Review network calls and API interactions to gracefully handle failures and retries.

