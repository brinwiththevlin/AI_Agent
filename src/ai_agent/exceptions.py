"""Custom exceptions for the AI Agent project."""

from enum import Enum, auto


class PathType(Enum):
    """Specifies the expected type of a file system path.

    Attributes:
        DIRECTORY: Represents the Directory type.
        FILE: Represents the File type.
    """

    DIRECTORY = auto()
    FILE = auto()


class AIAgentError(Exception):
    """Base exception for all custom errors in this project."""


class DirectoryTraversalError(AIAgentError):
    """Raised when a file path attempts to access a location outside the allowed directory.

    This error is a security measure to prevent the agent from accessing
    unauthorized parts of the file system.

    Attributes:
        target_path (str): The invalid path that triggered the error.
    """

    def __init__(self, target_path: str) -> None:
        """Initializes the DirectoryTraversalError.

        Args:
            target_path: The file path that attempted to traverse directories.
        """
        self.target_path: str = target_path
        message = f"Directory traversal of '{self.target_path}' is not allowed."
        super().__init__(message)


class InvalidPathError(AIAgentError):
    """Raised when a path does not exist or is not the expected type (file or directory).

    Attributes:
        target_path (str): The path that was found to be invalid.
    """

    def __init__(self, target_path: str, path_type: PathType = PathType.DIRECTORY) -> None:
        """Initializes the InvalidPathError.

        Args:
            target_path: The path that was found to be invalid.
            path_type: The type of path that was expected.
        """
        self.target_path: str = target_path
        message = f"The path '{self.target_path}' is not a valid {path_type.name.lower()}."
        super().__init__(message)


class ApiKeyError(AIAgentError):
    """Raised when there is a problem with the API key."""

    def __init__(self) -> None:
        """Initializes the ApiKeyError."""
        message = "GEMINI_API_KEY not found in environment variables or .env file."
        super().__init__(message)
