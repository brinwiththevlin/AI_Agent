"""Package for working with files."""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def get_files_info(working_directory: str | Path, directory: str | Path = ".") -> str:
    """Get info on all files in a directory.

    Directory must be a descendant of the working directory. Inspecting outside
    of the working directory is explicitly prohibited to prevent security risks.

    Args:
        working_directory: The highest-level directory where inspection is allowed.
        directory: The specific directory to inspect, relative to the working_directory.

    Returns:
        A formatted string containing information about the files.

    Raises:
        ValueError: If the target directory is outside the working directory.
        FileNotFoundError: If the target directory does not exist.
        NotADirectoryError: If the target path is not a directory.
    """
    logger.debug(f"New request: working='{working_directory}', dir='{directory}'")

    try:
        base_path = Path(working_directory).resolve(strict=True)

        target_path = (base_path / directory).resolve(strict=True)

        if not target_path.is_relative_to(base_path):
            msg = f"Directory traversal of {target_path} is not allowed."
            raise ValueError(msg)

        if not target_path.is_dir():
            msg = f"'{target_path}' is not a directory."
            raise NotADirectoryError(msg)

    except FileNotFoundError as e:
        logger.exception(f"Path not found: {e}")
        raise
    except ValueError as e:
        logger.exception(f"Security error: {e}")
        raise

    # 5. Iterate and build the report.
    reports: list[str] = []
    for file in target_path.iterdir():
        # Using a try-except block here is good practice in case of
        # permission errors on a specific file.
        try:
            file_report = f"- {file.name}: file_size={file.stat().st_size} bytes, is_dir={file.is_dir()}"
            reports.append(file_report)
        except OSError as e:
            logger.warning(f"Could not stat file {file.name}: {e}")

    return "\n".join(reports)
