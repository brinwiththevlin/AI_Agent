"""Entry point for boot_dev submissions."""

import logging
import sys

from ai_agent.main import main

if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    EXPECTED_ARG_COUNT = 2

    if len(sys.argv) < EXPECTED_ARG_COUNT:
        logger.critical("no promt given")
        sys.exit(1)
    prompt = sys.argv[1]
    main(prompt)
