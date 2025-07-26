"""Tools for interacting with the local file system.

This module provides a safe, agent-callable function for reading files.
"""

import logging

from ai_agent.constants import FILE_CHAR_LIMIT
from ai_agent.exceptions import AIAgentError, PathType
from ai_agent.functions.utils import validate_path

logger = logging.getLogger(__name__)


def get_file_content(working_directory: str, file_path: str) -> str:
    """Reads the content of a file up to a character limit.

    This function is designed to be safe for use by an LLM agent. It will always
    return a string. On success, it returns the file content. On failure, it
    returns a string starting with "Error: ".

    Args:
        working_directory: The highest-level directory where reading is allowed.
        file_path: The path to the file to read, relative to the working directory.

    Returns:
        str: The content of the file or an error message.
    """
    try:
        target_path = validate_path(file_path, working_directory, expected_type=PathType.FILE)

        with target_path.open(encoding="utf-8") as f:
            content = f.read(FILE_CHAR_LIMIT)
            # Check if there's more content
            if f.read(1):
                content += f"\n[ ... File '{file_path}' truncated at {FILE_CHAR_LIMIT} characters ... ]"
    except (OSError, AIAgentError) as e:
        logger.exception("Error in get_file_content:")
        return f"Error: {e}"
    else:
        return content
