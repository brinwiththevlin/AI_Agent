"""Calculator class."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


class Calculator:
    """Calculator Class."""

    def __init__(self) -> None:
        """Initiallizer for the calculator."""
        self.operators: dict[str, Callable[[float, float], float]] = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        self.precedence: dict[str, int] = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }

    def evaluate(self, expression: str) -> float | None:
        """Evaluates expresion passed into the calculator.

        Evaluates the entire expresion. only handels basic arithmatic. expresion must be space delimeted.
        ex: "1 + 2 / 4". not "1+2/4".

        Args:
            expression: expresion to evaluate

        Returns:
            final value, None if expresion is malformated
        """
        if not expression or expression.isspace():
            return None
        tokens = expression.strip().split()
        return self._evaluate_infix(tokens)

    def _evaluate_infix(self, tokens: list[str]) -> float:
        values: list[float] = []
        operators: list[str] = []

        for token in tokens:
            if token in self.operators:
                while (
                    operators
                    and operators[-1] in self.operators
                    and self.precedence[operators[-1]] >= self.precedence[token]
                ):
                    self._apply_operator(operators, values)
                operators.append(token)
            else:
                try:
                    values.append(float(token))
                except ValueError as e:
                    msg = f"invalid token: {token}"
                    raise ValueError(msg) from e

        while operators:
            self._apply_operator(operators, values)

        if len(values) != 1:
            msg = "invalid expression"
            raise ValueError(msg)

        return values[0]

    def _apply_operator(self, operators: list[str], values: list[float]) -> None:
        if not operators:
            return

        operator = operators.pop()
        if len(values) < 2:  # noqa: PLR2004
            msg = f"not enough operands for operator {operator}"
            raise ValueError(msg)

        b = values.pop()
        a = values.pop()
        values.append(self.operators[operator](a, b))
