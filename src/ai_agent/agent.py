"""First AI agent project."""

import logging
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from ai_agent.constants import (
    BASE_SYSTEM_PROMPT,
    EXCLUDED_FUNCTION_MODULES,
    MAX_ITERATIONS,
    MODEL_NAME,
    WORKING_DIRECTORY,
)
from ai_agent.discovery import discover_tools, generate_schema
from ai_agent.exceptions import ApiKeyError, FunctionError

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
    system_prompt = generate_system_prompt()

    if verbose:
        print(f"User prompt: {user_prompt}")

    _ = load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ApiKeyError
    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    iters = 0
    while True:
        iters += 1
        if iters > MAX_ITERATIONS:
            print(f"Maximum iterations ({MAX_ITERATIONS}) reached.")
            sys.exit(1)

        try:
            final_response = generate_content(client, messages, system_prompt, verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")


def generate_content(
    client: genai.Client, messages: list[types.Content], system_prompt: str, verbose: bool
) -> str | None:
    """Generate conent to display to the screen.

    Args:
        client: ai client used to generate content
        messages: message history
        system_prompt: Prompt to give the client
        verbose: set to True for stats for nerds.

    Returns:
        final response

    Raises:
        FunctionError: raises  if function call result is empty or there was no function calls
    """
    response = client.models.generate_content(  # pyright: ignore[reportUnknownMemberType]
        model=MODEL_NAME,
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[AVAILABLE_FUNCTIONS]),
    )
    if response.candidates:
        messages.extend([c.content for c in response.candidates if c.content])
    if verbose:
        if response.usage_metadata is None:
            msg = "usage_metadata is a required field for this project"
            raise AttributeError(msg)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if not response.function_calls:
        return response.text

    function_responses: list[types.Part] = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if not function_call_result.parts or not function_call_result.parts[0].function_response:
            raise FunctionError(function_call_part.name)
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise FunctionError()

    messages.append(types.Content(role="tool", parts=function_responses))
    return None


def generate_system_prompt() -> str:
    """Generates the system promped based on available functions.

    Returns:
        string for the full system prompt
    """
    if not AVAILABLE_FUNCTIONS.function_declarations:
        tool_descriptions = ["no functions available at this time"]
    else:
        tool_descriptions: list[str] = [
            func.description.split("\n")[0] for func in AVAILABLE_FUNCTIONS.function_declarations if func.description
        ]
    return BASE_SYSTEM_PROMPT.format(tool_list="\n- ".join(tool_descriptions))


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
        print(f"Calling function: {function_call_part.name}")

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
