"""First AI agent project."""

import logging
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

logging.basicConfig(
    filename="app.log", filemode="w", level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def run_agent(user_prompt: str, verbose: bool) -> None:
    """Main driver for AI agent project.

    Cli application to interact with an LLM in the terminal.

    Args:
        user_prompt: Prompt to ask the AI.
        verbose: Set to true if you want token stats in your response.
    """
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    _ = load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    print(response.text)

    if verbose:
        if response.usage_metadata is None:
            logger.fatal("usage_metadata is a required field for this project")
            sys.exit(1)

        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count

        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

