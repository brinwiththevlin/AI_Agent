"""Custom exceptions for the AI Agent project."""


class AIAgentError(Exception):
    """Base exception for all custom errors in this project."""


class DirectoryTraversalError(AIAgentError):
    """Raised when a directory traversal attempt is detected."""

    def __init__(self, target_path: str) -> None:
        self.target_path: str = target_path
        message = f"Directory traversal of '{self.target_path}' is not allowed."
        super().__init__(message)


class InvalidPathError(AIAgentError):
    """Raised when a path is not a valid directory."""

    def __init__(self, target_path: str, directory: bool = True) -> None:
        self.target_path: str = target_path
        message = f"The path '{self.target_path}' is not a valid {'directory' if directory else 'file'}."
        super().__init__(message)
