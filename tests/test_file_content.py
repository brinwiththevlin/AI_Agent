import unittest

from ai_agent.constants import FILE_CHAR_LIMIT
from ai_agent.functions.get_file_content import get_file_content

from .utils import WORKING_DIR


class TestFileContent(unittest.TestCase):
    """Test suite for the get_file_content function."""

    def test_lorum_ipsum(self) -> None:
        """Test for the lorum ipsum file. contains 20,000 bytes."""
        result = get_file_content(WORKING_DIR, "lorum_ipsum.txt")
        print(result)
        self.assertRegex(result, r"\[ \.\.\. File .* truncated at " + str(FILE_CHAR_LIMIT) + r" characters \.\.\. \]")

    def test_calculator(self) -> None:
        """Test for the calc.py file."""
        result = get_file_content(WORKING_DIR, "pkg/calculator.py")
        print(result)
        self.assertFalse(result.startswith("Error:"), f"unexpected error: {result}")
        self.assertNotRegex(
            result, r"\[ \.\.\. File .* truncated at " + str(FILE_CHAR_LIMIT) + r" characters \.\.\. \]"
        )

    def test_calc_main(self) -> None:
        """Test for the main.py file."""
        result = get_file_content(WORKING_DIR, "main.py")
        print(result)
        self.assertFalse(result.startswith("Error:"))
        self.assertNotRegex(
            result, r"\[ \.\.\. File .* truncated at " + str(FILE_CHAR_LIMIT) + r" characters \.\.\. \]"
        )

    def test_prohibited_file(self) -> None:
        """Test for the out of bounds /bin/cat file."""
        result = get_file_content(WORKING_DIR, "/bin/cat")
        print(result)
        self.assertTrue(result.startswith("Error:"))

    def test_none_existent_file(self) -> None:
        """Test for the non existant does_not_exist.py file."""
        result = get_file_content(WORKING_DIR, "does_not_exist.py")
        print(result)
        self.assertTrue(result.startswith("Error:"))


if __name__ == "__main__":
    _ = unittest.main()
