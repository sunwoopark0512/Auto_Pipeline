# Auto Pipeline

This repository contains automation scripts for content generation and Notion uploading.

## Script Placement Rules

All pipeline step modules should live either in the repository root or in the `scripts/` directory. Each module name without the `.py` extension must be unique across both locations.


## Wheel Artifacts

Application wheels are not committed to the repository. They are built automatically whenever a GitHub release is published and are attached as release assets. To install the latest version directly from GitHub, run:

```bash
pip install --upgrade auto_pipeline \
  -f https://github.com/your-org/Auto_Pipeline/releases/latest/download
```

## Releases

Version numbers follow [Semantic Versioning](https://semver.org). New
tags and changelog entries are generated automatically by the
`release-please` workflow whenever changes are pushed to `main`.

## Deployment

The `main-pipeline` workflow deploys to both `staging` and `prod`
environments. Each environment runs the pipeline, reports metrics to
Datadog, and notifies Slack on failure.

### Running in Dry Run Mode

Verify imports without executing steps:

```bash
python run_pipeline.py --dry-run
```

