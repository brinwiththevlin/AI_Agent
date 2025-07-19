"""Calculator package."""

import argparse
from argparse import Namespace

from ai_agent.calculator.pkg.calculator import Calculator
from ai_agent.calculator.pkg.render import render


class CalcArgs(Namespace):
    """Typing information for arguments."""

    expression: list[str]

    def __init__(self) -> None:
        """Initialize the namespace, setting defaults for type checkers."""
        super().__init__()
        self.expression = []


def main() -> None:
    """Example usage of the Calculator package."""
    parser = argparse.ArgumentParser(
        description="A command-line calculator.",
        epilog='Example: python main.py "3 + 5"',
    )

    _ = parser.add_argument(
        "expression",
        type=str,
        nargs="+",
        help="The mathematical expression to evaluate, in quotes.",
    )
    args = parser.parse_args(namespace=CalcArgs())

    calculator = Calculator()
    expression = " ".join(args.expression)
    try:
        result = calculator.evaluate(expression)
        to_print = render(expression, result)
        print(to_print)
    except Exception as e:  # noqa: BLE001
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
