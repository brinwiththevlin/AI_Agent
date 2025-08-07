"""Configuration file with all global constants."""

import os
from typing import Final

# Static application constants (rarely change)
DEFAULT_FILE_CHAR_LIMIT: Final[int] = 10_000
DEFAULT_MODEL_NAME: Final[str] = "gemini-2.0-flash-001"
DEFAULT_WORKING_DIRECTORY: Final[str] = "src/ai_agent/calculator"
DEFAULT_LOG_LEVEL: Final[str] = "INFO"

# Environment-configurable values with defaults
FILE_CHAR_LIMIT: int = int(os.environ.get("FILE_CHAR_LIMIT", DEFAULT_FILE_CHAR_LIMIT))
MODEL_NAME: str = os.environ.get("MODEL_NAME", DEFAULT_MODEL_NAME)
WORKING_DIRECTORY: str = os.environ.get("WORKING_DIRECTORY", DEFAULT_WORKING_DIRECTORY)
LOG_LEVEL: str = os.environ.get("LOG_LEVEL", DEFAULT_LOG_LEVEL)

# Static templates and prompts (not environment-specific)
BASE_SYSTEM_PROMPT: Final[str] = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, ALWAYS make a function call plan then execute that plan.
Do not ask the user for more information without first making a plan. You can perform the following operations:

- {tool_list}

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# Business logic constants
MAX_FUNCTION_TIMEOUT: Final[int] = 30
SUPPORTED_FILE_EXTENSIONS: Final[list[str]] = [".py", ".txt", ".md"]
EXCLUDED_FUNCTION_MODULES: Final[list[str]] = ["utils"]
LOG_FILENAME: Final[str] = "app.log"
MAX_ITERATIONS = 20
