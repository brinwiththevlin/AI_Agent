"""First AI agent project."""

import logging
import os
import sys

from dotenv import load_dotenv
from google import genai

logger = logging.getLogger(__name__)


def main(prompt: str) -> None:
    """Main script for AI agent project."""

    _ = load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=prompt,
    )

    if response.usage_metadata is None:
        logger.fatal("usage_metadata is a required field for this project")
        sys.exit(1)

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    print(response.text)
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")


