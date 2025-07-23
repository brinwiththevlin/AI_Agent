"""Tools for interacting with the local file system.

This module provides a safe, agent-callable function for querying files.
"""

import logging
from pathlib import Path

from ai_agent.exceptions import AIAgentError, PathType
from ai_agent.functions.utils import validate_path

logger = logging.getLogger(__name__)


def get_files_info(working_directory: str | Path, directory: str | Path = ".") -> str:
    """Get info on all files in a directory.

    This function is designed to be safe for use by an LLM agent. It will always
    return a string. On success, it returns file information. On failure, it
    returns a string starting with "Error: ".

    Args:
        working_directory (str| Path): The highest-level directory where inspection is allowed.
        directory (str| Path): The specific directory to inspect, relative to the working_directory.

    Returns:
        str: A formatted string containing file information or an error message.
    """
    logger.debug(f"New request: working='{working_directory}', dir='{directory}'")

    try:
        target_path = validate_path(directory, working_directory, expected_type=PathType.DIRECTORY)

    except (FileNotFoundError, AIAgentError) as e:
        logger.exception("Error in get_files_info:")
        return f"Error: {e}"

    reports: list[str] = []
    for file in sorted(target_path.iterdir()):
        try:
            file_report = f"- {file.name}: file_size={file.stat().st_size} bytes, is_dir={file.is_dir()}"
            reports.append(file_report)
        except OSError as e:
            logger.warning(f"Could not stat file {file.name}: {e}")

    return "\n".join(reports)
