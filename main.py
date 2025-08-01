"""Entry point for boot_dev submissions."""

import argparse
import logging
from argparse import Namespace

from ai_agent.agent import run_agent
from ai_agent.constants import LOG_FILENAME, LOG_LEVEL
from ai_agent.exceptions import ApiKeyError

logging.basicConfig(
    filename=LOG_FILENAME,
    filemode="w",
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


class AiArgs(Namespace):
    """Typing information for arguments."""

    prompt: str = ""
    verbose: bool = False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Agent CLI")
    _ = parser.add_argument("prompt", type=str, help="The prompt for the AI agent.")
    _ = parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output."
    )

    try:
        args = parser.parse_args(namespace=AiArgs())
        logger.info(f"Arguments received: {args}")
        print(run_agent(args.prompt, verbose=args.verbose))
    except ApiKeyError:
        logger.exception("make sure you have an API key")
    except SystemExit:
        logger.critical("Failed to parse arguments. Check the command.")
