import unittest

from ai_agent.functions.run_python_file import run_python_file

from .utils import WORKING_DIR


class TestRunPython(unittest.TestCase):
    """Test suite for run_python_file."""

    def test_main(self) -> None:
        result = run_python_file(WORKING_DIR, "calc.py")
        print(result)
        self.assertIn("usage:", result)

    def test_main_with_args(self) -> None:
        result = run_python_file(WORKING_DIR, "calc.py", ["3 + 5"])
        print(result)
        self.assertIn("8", result)

    def test_parent(self) -> None:
        result = run_python_file(WORKING_DIR, "../main.py")
        print(result)
        self.assertRegex(result, r"Error: Cannot execute ")

    def test_non_existent_python(self) -> None:
        result = run_python_file(WORKING_DIR, "nonexistent.py")
        print(result)
        self.assertRegex(result, r"Error: .*")


if __name__ == "__main__":
    _ = unittest.main()
