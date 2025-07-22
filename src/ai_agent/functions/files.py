"""Package for working with files."""

import logging
from pathlib import Path

from ai_agent.config import FILE_CHAR_LIMIT
from ai_agent.exceptions import AIAgentError, DirectoryTraversalError, InvalidPathError

logger = logging.getLogger(__name__)


def get_files_info(working_directory: str | Path, directory: str | Path = ".") -> str:
    """Get info on all files in a directory.

    This function is designed to be safe for use by an LLM agent. It will always
    return a string. On success, it returns file information. On failure, it
    returns a string starting with "Error: ".

    Args:
        working_directory: The highest-level directory where inspection is allowed.
        directory: The specific directory to inspect, relative to the working_directory.

    Returns:
        A formatted string containing file information or an error message.
    """
    logger.debug(f"New request: working='{working_directory}', dir='{directory}'")

    try:
        base_path = Path(working_directory).resolve(strict=True)
        target_path = (base_path / directory).resolve(strict=True)

        if not target_path.is_relative_to(base_path):
            raise DirectoryTraversalError(str(target_path))

        if not target_path.is_dir():
            raise InvalidPathError(str(target_path))

        reports: list[str] = []
        for file in sorted(target_path.iterdir()):
            try:
                file_report = f"- {file.name}: file_size={file.stat().st_size} bytes, is_dir={file.is_dir()}"
                reports.append(file_report)
            except OSError as e:
                logger.warning(f"Could not stat file {file.name}: {e}")

        return "\n".join(reports)

    except (FileNotFoundError, AIAgentError) as e:
        logger.exception("Error in get_files_info:")
        return f"Error: {e}"


def get_file_content(working_directory: str | Path, file_path: str | Path) -> str:
    """Reads the content of a file up to a character limit.

    This function is designed to be safe for use by an LLM agent. It will always
    return a string. On success, it returns the file content. On failure, it
    returns a string starting with "Error: ".

    Args:
        working_directory: The highest-level directory where reading is allowed.
        file_path: The path to the file to read, relative to the working directory.

    Returns:
        The content of the file or an error message.
    """
    try:
        base_path = Path(working_directory).resolve(strict=True)
        target_path = (base_path / file_path).resolve(strict=True)

        if not target_path.is_relative_to(base_path):
            raise DirectoryTraversalError(str(target_path))

        if not target_path.is_file():
            raise InvalidPathError(str(target_path), directory=False)

        with Path.open(target_path, encoding="utf-8") as f:
            content = f.read(FILE_CHAR_LIMIT)
            # Check if there's more content
            if f.read(1):
                content += f"\n[ ... File '{file_path}' truncated at {FILE_CHAR_LIMIT} characters ... ]"
    except Exception as e:
        logger.exception("Error in get_file_content:")
        return f"Error: {e}"
    else:
        return content
