"""First AI agent project."""

import logging
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from ai_agent.constants import (
    BASE_SYSTEM_PROMPT,
    EXCLUDED_FUNCTION_MODULES,
    MODEL_NAME,
    WORKING_DIRECTORY,
)
from ai_agent.discovery import discover_tools, generate_schema
from ai_agent.exceptions import ApiKeyError

logger = logging.getLogger(__name__)


DISCOVERED_TOOLS = discover_tools(exclude=EXCLUDED_FUNCTION_MODULES)
AVAILABLE_FUNCTIONS = types.Tool(
    function_declarations=generate_schema(DISCOVERED_TOOLS, banned_args=["working_directory"])
)


def run_agent(user_prompt: str, verbose: bool) -> None:
    """Main driver for AI agent project.

    Cli application to interact with an LLM in the terminal.

    Args:
        user_prompt (str): Prompt to ask the AI.
        verbose (bool): Set to true if you want token stats in your response.
    """
    # generate system prompt

    if not AVAILABLE_FUNCTIONS.function_declarations:
        tool_descriptions = ["no functions available at this time"]
    else:
        tool_descriptions: list[str] = [
            func.description.split("\n")[0] for func in AVAILABLE_FUNCTIONS.function_declarations if func.description
        ]
    system_prompt = BASE_SYSTEM_PROMPT.format(tool_list="\n- ".join(tool_descriptions))

    _ = load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ApiKeyError
    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(  # pyright: ignore[reportUnknownMemberType]
        model=MODEL_NAME,
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[AVAILABLE_FUNCTIONS]),
    )

    if response.function_calls:
        for f in response.function_calls:
            print(f"Calling function: {f.name}({f.args})")
    elif response.text:
        print(response.text)

        if verbose:
            if response.usage_metadata is None:
                msg = "usage_metadata is a required field for this project"
                raise AttributeError(msg)

            prompt_tokens = response.usage_metadata.prompt_token_count
            response_tokens = response.usage_metadata.candidates_token_count

            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")


def call_function(function_call_part: types.FunctionCall, verbose: bool = False) -> types.Content:
    """Call function based on the function call part.

    Args:
        function_call_part: The function call part containing the function name and arguments.
        verbose: If True, print additional information. Defaults to False.

    Returns:
        types.Content: Response from the function call.
    """
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    if function_call_part.name not in DISCOVERED_TOOLS:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name or "unknown_function",
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    if function_call_part.args is None:
        function_call_part.args = {}
    function_call_part.args["working_directory"] = WORKING_DIRECTORY
    func = DISCOVERED_TOOLS[function_call_part.name]
    result = func(**function_call_part.args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name or "unknown_function",
                response={"result": result},
            )
        ],
    )
