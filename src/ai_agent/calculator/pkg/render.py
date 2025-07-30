"""math expression renderer."""

# render.py


def render(expression: str, result: float | None) -> str:
    """Redneres a box with the answer from the expression.

    Args:
        expression: expression that was evalueated
        result: final result of expression

    Returns:
        str: ASCII box with expresion and result inside
    """
    result_str = str(int(result)) if isinstance(result, float) and result.is_integer() else str(result)

    box_width = max(len(expression), len(result_str)) + 4

    box: list[str] = []
    box.append("┌" + "─" * box_width + "┐")
    box.append("│" + " " * 2 + expression + " " * (box_width - len(expression) - 2) + "│")
    box.append("│" + " " * box_width + "│")
    box.append("│" + " " * 2 + "=" + " " * (box_width - 3) + "│")
    box.append("│" + " " * box_width + "│")
    box.append("│" + " " * 2 + result_str + " " * (box_width - len(result_str) - 2) + "│")
    box.append("└" + "─" * box_width + "┘")
    return "\n".join(box)
