# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]
- Automated release tagging via Release Please
- Multi-environment CI pipeline with Datadog metrics
- Weekly secret rotation workflow
- Pylint and mypy checks integrated
- Structured logging and failure notification in `run_pipeline.py`
- Wheels built and uploaded as release assets
- Wheel build job runs on multiple OS and Python versions
- Added installation instructions for wheels in README
- `run_pipeline.py` now supports `--dry-run` and detects duplicate modules
- `--dry-run` also sets `DRY_RUN=1` for downstream steps
- Improved duplicate detection using `Path.samefile`
- Improved caching in wheel build workflow
