"""Tools for interacting with the local file system.

This module provides a safe, agent-callable function for writing to a file.
"""

import logging
from pathlib import Path

from ai_agent.exceptions import AIAgentError, PathType
from ai_agent.functions.utils import validate_path

logger = logging.getLogger(__name__)


def write_file(working_directory: str, file_path: str, content: str) -> str:
    """Tool for agent to write to a file.

    Overriddes the content of a file within the working directory. Creates a new file if it does not exist.

    Args:
        working_directory: Path for the working directory
        file_path: Path relative to the working directory that is to be created/overwriten
        content: content to write to the file

    Returns:
        str: Success or Error message as a string.
    """
    try:
        target_path = validate_path(file_path, working_directory, expected_type=PathType.FILE)
    except FileNotFoundError:
        base_path = Path(working_directory).resolve()
        target_path = (base_path / file_path).resolve()
        target_path.parent.mkdir(parents=True, exist_ok=True)
    except (AIAgentError, OSError) as e:
        logger.exception("Error in write_file:")
        return f"Error: {e}"

    try:
        with Path.open(target_path, "w") as f:
            bit_len = f.write(content)
            return f"Successfully wrote to '{file_path}' ({bit_len} characters written)"
    except OSError as e:
        logger.exception("Error in write_file:")
        return f"Error: {e}"
