"""Tools for interacting with the local file system.

This module provides a safe, agent-callable function for running a python file.
"""

import logging
import sys
from subprocess import run
from typing import Any

from ai_agent.constants import MAX_FUNCTION_TIMEOUT, SUPPORTED_FILE_EXTENSIONS
from ai_agent.exceptions import DirectoryTraversalError, PathType
from ai_agent.functions.utils import validate_path

logger = logging.getLogger(__name__)


def run_python_file(working_directory: str, file_path: str, args: list[Any] | None = None) -> str:  # pyright: ignore[reportExplicitAny]
    """Tool to allow agent to execute python code stored in the working directory.

    Only python code stored in teh working directoyr is allowed to be run.

    Args:
        working_directory: the working_directory
        file_path: file path must be a decendent of working_directory and be a python file
        args: comand arguemts to the python function

    Returns:
        str: output of the python funciton being ran by the ai agent.
    """
    if args is None:
        args = []
    try:
        target_path = validate_path(file_path, working_directory, expected_type=PathType.FILE)
    except DirectoryTraversalError:
        logger.exception("Error in run_python_file:")
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not target_path.exists():
        logger.exception("Error in run_python_file:")
        return f'Error: File "{file_path}" not found.'
    if not target_path.name.endswith(SUPPORTED_FILE_EXTENSIONS[0]):  # .py extension
        return f'Error: "{file_path}" is not a Python file.'

    try:
        # WARNING: security concern. This runs arbitrary code, which could be dangerous.
        process = run(  # noqa: S603
            [sys.executable, target_path, *args],
            text=True,
            check=False,
            capture_output=True,
            timeout=MAX_FUNCTION_TIMEOUT,
        )

        if not process.stdout and not process.stderr:
            return "No output produced"

        output = ""
        output += f"STDOUT: {process.stdout}\n"
        output += f"STDERR: {process.stderr}\n"
        if process.returncode != 0:
            output += f"Process exited with code {process.returncode}"
    except Exception as e:  # noqa: BLE001
        return f"Error: excecuting Python file: {e}"

    return output
