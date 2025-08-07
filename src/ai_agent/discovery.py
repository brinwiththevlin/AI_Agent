"""Package for generating FunctionDeclaration schemas for the google.genai API to be able to run functions."""

import importlib
import inspect
import logging
import pkgutil
from collections.abc import Callable
from enum import Enum
from typing import Any

from google.genai import types

import ai_agent.functions
from ai_agent.constants import EXCLUDED_FUNCTION_MODULES, LOG_FILENAME, LOG_LEVEL

logger = logging.getLogger(__name__)

TYPE_MAPPING: dict[Any, types.Type] = {  # pyright: ignore[reportExplicitAny]
    str: types.Type.STRING,
    int: types.Type.INTEGER,
    float: types.Type.NUMBER,
    bool: types.Type.BOOLEAN,
    list: types.Type.ARRAY,
}


# This new function does the slow work just ONCE.
def discover_tools(
    exclude: list[str] | None = None,
) -> dict[str, Callable[..., str]]:
    """Discovers tools found in the functions directory.

    Uses the builtin inspect module to discover all functions in the functions directory.
    Returns only the funtions the match the title of their file.

    Args:
        exclude: files to exlude from inspection. do not use the full path, do not use the ".py" file extention

    Returns:
        dict of callable functions
    """
    discovered_tools: dict[str, Callable[..., str]] = {}
    package_path = ai_agent.functions.__path__
    package_prefix = ai_agent.functions.__name__ + "."

    for _, module_name, _ in pkgutil.iter_modules(package_path, package_prefix):
        file_name = module_name.split(".")[-1]
        if exclude and file_name in exclude:
            continue

        module = importlib.import_module(module_name)
        members = inspect.getmembers(module, inspect.isfunction)

        function_names = [m[0] for m in members]
        try:
            primary_function_idx = function_names.index(file_name)
        except ValueError:
            logger.exception("module file does not have a function of the same name")
            continue

        primary_func_name, primary_func_object = members[primary_function_idx]
        discovered_tools[primary_func_name] = primary_func_object

    return discovered_tools


def generate_schema(
    discovered_tools: dict[str, Callable[..., str]],
    banned_args: list[str] | None = None,
) -> list[types.FunctionDeclaration]:
    """Creates a genai.types.FunctionDeclaration schema for all tool functions found in the funcitons directory.

    Some files in that directory are not tools so you cna exclude some names.
    This tool assumes that public functions have Google Python style DocStrings.

    Returns:
        list: list of FunctionDeclarations.
    """
    schemas: list[types.FunctionDeclaration] = []

    for name, func in discovered_tools.items():
        docstring = inspect.getdoc(func)
        signature = inspect.signature(func)

        if not docstring:
            logger.info(f"module function '{name}' lacks a docstring, could not generate schema")
            continue
        description, parameter_info = _parse_docstring(docstring, banned_args)

        param_schema = _get_parameter_schema(parameter_info, signature, banned_args)
        s = types.FunctionDeclaration(name=name, description=description, parameters=param_schema)
        schemas.append(s)

    return schemas


def _parse_docstring(docstring: str, banned_args: list[str] | None) -> tuple[str, dict[str, str]]:
    if banned_args is None:
        banned_args = []

    lines = docstring.strip().split("\n")

    description_lines: list[str] = []
    args_dict: dict[str, str] = {}

    parsing = Enum("Parsing", [("DESC", 1), ("ARGS", 2), ("RETURNS", 3)])
    parsing_section = parsing.DESC

    idx = 0
    while idx < len(lines):
        line = lines[idx]
        stripped_line = line.strip()
        if stripped_line.startswith("Args:"):
            parsing_section = parsing.ARGS
            idx += 1
            args_dict, idx = _parse_args_section(lines, idx, banned_args)
            parsing_section = parsing.RETURNS
            continue
        if parsing_section == parsing.DESC:
            description_lines.append(line)
        idx += 1

    return "\n".join(description_lines).strip(), args_dict


def _parse_args_section(lines: list[str], start_idx: int, banned_args: list[str]) -> tuple[dict[str, str], int]:
    args_dict: dict[str, str] = {}
    arg_name = ""
    long_desc: list[str] = []
    idx = start_idx
    while idx < len(lines):
        stripped_line = lines[idx].strip()
        if stripped_line.startswith("Returns:"):
            if arg_name and arg_name not in banned_args:
                args_dict[arg_name.strip()] = " ".join(long_desc).strip()
            break
        if ":" in stripped_line:
            if arg_name and arg_name not in banned_args:
                args_dict[arg_name.strip()] = " ".join(long_desc).strip()
            arg_name, arg_desc = stripped_line.split(":", maxsplit=1)
            long_desc = [arg_desc.strip()]
        elif stripped_line:
            long_desc.append(stripped_line)
        idx += 1
    if arg_name and arg_name not in banned_args:
        args_dict[arg_name.strip()] = " ".join(long_desc).strip()
    return args_dict, idx


def _get_parameter_schema(
    parameter_info: dict[str, str],
    signature: inspect.Signature,
    banned_args: list[str] | None = None,
) -> types.Schema:
    if banned_args is None:
        banned_args = []
    properties: dict[str, types.Schema] = {}
    for p in signature.parameters.values():
        desc = parameter_info.get(p.name, "")
        if not desc and p.name not in banned_args:
            logger.warning(f"parameter {p} does not have any documentation")

        properties[p.name] = types.Schema(
            type=TYPE_MAPPING.get(p.annotation, types.Type.OBJECT),  # pyright: ignore[reportAny]
            description=desc,
        )

    return types.Schema(type=types.Type.OBJECT, properties=properties)


if __name__ == "__main__":
    logging.basicConfig(
        filename=LOG_FILENAME,
        filemode="a",
        level=getattr(logging, LOG_LEVEL),  # pyright: ignore[reportAny]
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    tools = discover_tools(exclude=EXCLUDED_FUNCTION_MODULES)
    _ = generate_schema(tools)
