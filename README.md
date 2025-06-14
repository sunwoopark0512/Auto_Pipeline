# Auto Pipeline

This repository contains automation scripts for content generation and Notion uploading.

## Script Placement Rules

All pipeline step modules should live either in the repository root or in the `scripts/` directory. Each module name without the `.py` extension must be unique across both locations.


## Wheel Artifacts

Application wheels are not committed to the repository. They are built automatically when a GitHub release is published and attached as release assets. You can download the latest wheel with:

```bash
gh release download <tag> -p "*.whl" -D wheels
```

