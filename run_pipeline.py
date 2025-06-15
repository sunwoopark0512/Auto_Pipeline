import argparse
import importlib
import os
import sys

import logging
import structlog


structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    processors=[
        structlog.processors.TimeStamper(fmt="ISO"),
        structlog.processors.add_log_level,
        structlog.processors.format_exc_info,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.JSONRenderer(),
    ],
)

logger = structlog.get_logger()

# Define the order of pipeline modules to execute
PIPELINE_SEQUENCE = [
    "hook_generator",
    "retry_failed_uploads",
    "retry_dashboard_notifier",
]

_loaded_origins: dict[str, str] = {}

def _import_and_run(module_name: str):
    """Import a module and run its main() function if present."""
    mod = importlib.import_module(module_name)
    origin = getattr(mod, "__file__", None)
    if origin:
        norm = os.path.realpath(origin)
        for name, seen in _loaded_origins.items():
            if seen == norm and name != module_name:
                raise ImportError(f"Module {module_name} duplicates {name}")
        _loaded_origins[module_name] = norm
    logger.info("\u2705 Imported %s", module_name)
    if os.getenv("DRY_RUN"):
        return
    if hasattr(mod, "main"):
        mod.main()


def main(args: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Import modules only")
    opts = parser.parse_args(args)

    if opts.dry_run:
        os.environ["DRY_RUN"] = "1"
        global logger
        logger = logger.bind(dry=True)
        logger.info("Import check only – no side-effects")

    for step in PIPELINE_SEQUENCE:
        _import_and_run(step)


if __name__ == "__main__":
    main()
