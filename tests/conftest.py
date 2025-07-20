"""Pytest configuration file.

This file runs automatically before any tests are executed.
It's the ideal place to set up project-wide test configurations,
like logging.
"""

import logging
from pathlib import Path

import pytest


@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    """Configures logging for the entire test session.

    This fixture runs once per test session. It sets up a single log file
    at the project's root directory, ensuring all logs from all tests go
    to the same place with a consistent format and level.
    """
    # Find the project root by looking for the pyproject.toml file
    project_root = Path(__file__).parent.parent
    log_file = project_root / "app.log"

    logging.basicConfig(
        level=logging.DEBUG,  # Set level to DEBUG to capture all messages
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        filename=str(log_file),  # Use the absolute path
        filemode="w",  # Overwrite the log file for each test run
    )

    logger = logging.getLogger(__name__)

    # Optional: Add a log message to indicate the start of a test session
    logger.info("=" * 20 + " TEST SESSION STARTED " + "=" * 20)  # noqa: G003
