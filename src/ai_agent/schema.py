"""Package for generating FunctionDeclaration schemas for the google.genai API to be able to run functions."""

import importlib
import inspect
import logging
import pkgutil
from enum import Enum
from typing import Any

from google.genai import types

import ai_agent.functions

logger = logging.getLogger(__name__)

TYPE_MAPPING: dict[Any, types.Type] = {  # pyright: ignore[reportExplicitAny]
    str: types.Type.STRING,
    int: types.Type.INTEGER,
    float: types.Type.NUMBER,
    bool: types.Type.BOOLEAN,
    list: types.Type.ARRAY,
}


def generate_schema(exclude: list[str] | None = None) -> list[types.FunctionDeclaration]:
    """Creates a genai.types.FunctionDeclaration schema for all tool functions found in the funcitons directory.

    Some files in that directory are not tools so you cna exclude some names.
    This tool assumes that public functions have Google Python style DocStrings.

    Args:
        exclude: list of file names to exclude. list of names should not include the whole
                 path nor the 'py' file extention

    Returns:
        list of FunctionDeclarations.
    """
    package_path = ai_agent.functions.__path__
    package_prefix = ai_agent.functions.__name__ + "."

    failed_packages: list[str] = []
    passed_packages: list[str] = []
    schemas: list[types.FunctionDeclaration] = []

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
            failed_packages.append(module_name)
            continue

        primary_func_name, primary_func_object = members[primary_function_idx]
        docstring = inspect.getdoc(primary_func_object)
        signature = inspect.signature(primary_func_object)

        if not docstring:
            logger.info(f"module {module_name} lacks a docstring, could not generate schema")
            failed_packages.append(module_name)
            continue
        description, parameter_info = _parse_docstring(docstring)

        param_schema = _get_parameter_schema(parameter_info, signature)
        s = types.FunctionDeclaration(name=primary_func_name, description=description, parameters=param_schema)
        schemas.append(s)
        passed_packages.append(module_name)

    logger.info(f"the following modules failed: {failed_packages}")
    logger.info(f"modules found: {passed_packages}")
    return schemas


def _parse_docstring(docstring: str) -> tuple[str, dict[str, str]]:
    # Split the docstring into lines
    lines = docstring.strip().split("\n")

    description_lines: list[str] = []
    args_dict: dict[str, str] = {}

    parsing = Enum("Parsing", [("DESC", 1), ("ARGS", 2), ("RETURNS", 3)])
    # Use a state machine to know which section we are in
    parsing_section = parsing.DESC  # Can be 'description', 'args', or 'returns'

    for line in lines:
        stripped_line = line.strip()

        if stripped_line.startswith("Args:"):
            parsing_section = parsing.ARGS
            continue
        if stripped_line.startswith("Returns:"):
            parsing_section = parsing.RETURNS
            continue

        if parsing_section == parsing.DESC:
            description_lines.append(line)
        if parsing_section == parsing.ARGS and ":" in stripped_line:
            arg_name, arg_desc = stripped_line.split(":", 1)  # Split only on the first colon
            args_dict[arg_name.strip()] = arg_desc.strip()
            # This logic could be expanded to handle multi-line descriptions

    return "\n".join(description_lines).strip(), args_dict


def _get_parameter_schema(parameter_info: dict[str, str], signature: inspect.Signature) -> types.Schema:
    properties: dict[str, types.Schema] = {}
    for p in signature.parameters.values():
        desc = parameter_info.get(p.name, "")
        if not desc:
            logger.warning(f"parameter {p} does not have any documentation")

        properties[p.name] = types.Schema(
            type=TYPE_MAPPING.get(p.annotation, types.Type.OBJECT),  # pyright: ignore[reportAny]
            description=desc,
        )

    return types.Schema(type=types.Type.OBJECT, properties=properties)


if __name__ == "__main__":
    logging.basicConfig(
        filename="app.log",
        filemode="w",
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    _ = generate_schema(exclude=["utils"])
