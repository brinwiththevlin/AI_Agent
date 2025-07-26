"""Package for working with files."""

import logging
from pathlib import Path

from ai_agent.exceptions import DirectoryTraversalError, InvalidPathError, PathType

logger = logging.getLogger(__name__)


def validate_path(relative_path: str, working_directory: str, expected_type: PathType) -> Path:
    """Method for validating the path.

    Relative_path must be relative to the working directory and must be a desendant.

    Args:
        relative_path: Path relative to the working directory.
        working_directory: Working directory. Traversal outside of this directory is prohibited.
        expected_type: expected type of the final path

    Returns:
        str: If the path is valid, the full target path is returned.

    Raises:
        DirectoryTraversalError: Raised if the full target path is out of scope.
        InvalidPathError: Raised if the path does not exist or the path is a dir and should be a file or vice versa.
    """
    base_path = Path(working_directory).resolve(strict=True)
    target_path = (base_path / relative_path).resolve()

    if not target_path.is_relative_to(base_path):
        raise DirectoryTraversalError(str(target_path))

    if (expected_type == PathType.DIRECTORY) != target_path.is_dir():
        raise InvalidPathError(str(target_path), path_type=expected_type)
    return target_path
