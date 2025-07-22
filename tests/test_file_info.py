"""Test cases for functions/files.py."""

import unittest
from pathlib import Path

from ai_agent.config import FILE_CHAR_LIMIT
from ai_agent.functions.files import get_file_content, get_files_info

FILE_PATH = Path(__file__)
PROJECT_ROOT = Path(__file__).parent.parent if FILE_PATH.parent.name == "tests" else Path(__file__).parent.parent.parent

WORKING_DIR = PROJECT_ROOT / "src" / "ai_agent" / "calculator"


class TestFileInfo(unittest.TestCase):
    """Test suite for the get_files_info function."""

    def test_list_calculator_directory(self) -> None:
        """Test listing the contents of the 'calculator' directory."""
        result = get_files_info(WORKING_DIR, ".")

        self.assertRegex(result, r"- __init__\.py: file_size=\d* bytes, is_dir=False")
        self.assertRegex(result, r"- main\.py: file_size=\d* bytes, is_dir=False")
        self.assertRegex(result, r"- calc\.py: file_size=\d* bytes, is_dir=False")
        self.assertRegex(result, r"- pkg: file_size=\d* bytes, is_dir=True")

    def test_list_pkg_subdirectory(self) -> None:
        """Test listing the contents of a subdirectory."""
        result = get_files_info(WORKING_DIR, "pkg")

        self.assertRegex(result, r"- __init__\.py: file_size=\d* bytes, is_dir=False")
        self.assertRegex(result, r"- calculator\.py: file_size=\d* bytes, is_dir=False")
        self.assertRegex(result, r"- render\.py: file_size=\d* bytes, is_dir=False")

    def test_prohibited_absolute_path(self) -> None:
        """Test that inspecting an absolute path outside the project raises an error."""
        result = get_files_info(WORKING_DIR, "/etc")
        self.assertIn("Error:", result)

    def test_prohibited_parent_directory(self) -> None:
        """Test that directory traversal ('../') is not allowed."""
        result = get_files_info(WORKING_DIR, "../")
        self.assertIn("Error:", result)

    def test_non_existent_directory(self) -> None:
        """Test that inspecting a non-existent directory raises an error."""
        result = get_files_info(WORKING_DIR, "this_dir_does_not_exist")
        self.assertIn("Error:", result)


class TestFileContent(unittest.TestCase):
    """Test quite for the get_file_content function."""

    def test_lorum_ipsum(self) -> None:
        """Test for the lorum ipsum file. contains 20,000 bytes."""
        result = get_file_content(WORKING_DIR, "lorum_ipsum.txt")
        self.assertRegex(result, r"\[ \.\.\. File .* truncated at .* characters \.\.\. \]")

    def test_calculator(self) -> None:
        """Test for the calc.py file."""
        result = get_file_content(WORKING_DIR, "pkg/calculator.py")
        self.assertFalse(result.startswith("Error:"), f"unexpected error: {result}")
        self.assertNotRegex(result, r"\[ \.\.\. File .* truncated at .* characters \.\.\. \]")

    def test_calc_main(self) -> None:
        """Test for the main.py file."""
        result = get_file_content(WORKING_DIR, "main.py")
        self.assertFalse(result.startswith("Error:"))
        self.assertNotRegex(result, r"\[ \.\.\. File .* truncated at .* characters \.\.\. \]")

    def test_prohibited_file(self) -> None:
        """Test for the out of bounds /bin/cat file."""
        result = get_file_content(WORKING_DIR, "/bin/cat")
        self.assertTrue(result.startswith("Error:"))

    def test_none_existent_file(self) -> None:
        """Test for the non existant does_not_exist.py file."""
        result = get_file_content(WORKING_DIR, "does_not_exist.py")
        self.assertTrue(result.startswith("Error:"))


if __name__ == "__main__":
    _ = unittest.main()
