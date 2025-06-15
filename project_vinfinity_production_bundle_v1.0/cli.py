"""Command-line interface for running the pipeline."""

import argparse
from pipeline_orchestrator import run_pipeline
from utils.init_env import load_env


def main() -> None:
    parser = argparse.ArgumentParser(description="Run content pipeline")
    parser.add_argument("topic", help="Topic to generate content for")
    args = parser.parse_args()

    env = load_env()
    run_pipeline(args.topic, env["WORDPRESS_API_TOKEN"])


if __name__ == "__main__":
    main()
