"""Package for working with files."""

import logging
from pathlib import Path

logging.basicConfig(
    filename="app.log", filemode="w", level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def get_files_info(working_directory: str | Path, directory: str | Path = ".") -> str:
    """Get info on all files in a directory.

    Directory must be a decendent of the working directory.
    Inspecting outisde of the working directory is explicitly prohibitied.

    Args:
        working_directory: highest level where inspecting is allowed
        directory: specific directory to inspect

    Returns:
        [TODO:description]
    """
    logger.debug(f"new request: working={working_directory}, dir={directory}")
    full_path = Path(working_directory).resolve() / directory
    logger.debug(f"full_path = {full_path}")
    if not full_path.resolve().is_relative_to(working_directory):
        logger.error(f"Error: Cannot list '{full_path}' as it is outside the permitted working directory")
        return f"Error: Cannot list '{full_path}' as it is outside the permitted working directory"

    if not full_path.is_dir():
        logger.error(f'Error: "{full_path}" is not a directory')
        return f"Error: '{full_path}' is not a directory"

    reports: list[str] = []
    for file in full_path.iterdir():
        file_report = f"- {file.name}: file_size={file.stat().st_size} bytes, is_dir={file.is_dir()}"
        reports.append(file_report)

    return "\n".join(reports)
