"""Launch a generated SaaS venture via the SaaS factory."""

import subprocess
from typing import Dict, Any

import yaml


def save_spec_to_yaml(spec: Dict[str, Any], path: str = "new_saas.yaml") -> None:
    """Save the given spec dictionary to a YAML file."""
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(spec, f, allow_unicode=True)


def launch_venture(spec: Dict[str, Any], spec_path: str = "new_saas.yaml") -> None:
    """Persist spec and trigger SaaS factory launcher."""
    save_spec_to_yaml(spec, spec_path)
    subprocess.run([
        "python",
        "saas_launcher.py",
        "--spec",
        spec_path,
    ], check=True)
