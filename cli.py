import argparse
import logging
from typing import List

from modules import generate_keywords
from modules import slack_notifier

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Auto pipeline CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    gen_parser = subparsers.add_parser("generate_keywords", help="Run keyword generator")
    gen_parser.add_argument("--notify", action="store_true", help="Send Slack notification")

    args = parser.parse_args(argv)

    if args.command == "generate_keywords":
        output_path = generate_keywords.run()
        logging.info("Generated keywords saved to %s", output_path)
        if args.notify:
            slack_notifier.send_slack_message(f"Keyword generation finished: {output_path}")


if __name__ == "__main__":
    main()
