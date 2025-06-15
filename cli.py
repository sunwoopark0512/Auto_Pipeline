import argparse
from pipeline_orchestrator import run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Content Automation Pipeline CLI")
    parser.add_argument("--topic", required=True, help="Enter the main topic to generate content")
    parser.add_argument("--token", required=True, help="WordPress or platform API token")

    args = parser.parse_args()
    run_pipeline(topic=args.topic, token=args.token)


if __name__ == "__main__":
    main()
