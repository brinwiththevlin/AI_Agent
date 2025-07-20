# tests/test_file_info.py

import unittest
from pathlib import Path

from ai_agent.functions.get_files_info import get_files_info

FILE_PATH = Path(__file__)
if FILE_PATH.parent.name == "tests":
    PROJECT_ROOT = Path(__file__).parent.parent
else:
    PROJECT_ROOT = Path(__file__).parent.parent.parent

WORKING_DIR = PROJECT_ROOT / "src" / "ai_agent" / "calculator"


class TestFiles(unittest.TestCase):
    """Test suite for the get_files_info function."""

    def test_list_calculator_directory(self):
        """Test listing the contents of the 'calculator' directory."""
        result = get_files_info(WORKING_DIR, ".")

        self.assertRegex(result, r"- __init__\.py: file_size=\d* bytes, is_dir=False")
        self.assertRegex(result, r"- main\.py: file_size=\d* bytes, is_dir=False")
        self.assertRegex(result, r"- calc\.py: file_size=\d* bytes, is_dir=False")
        self.assertRegex(result, r"- pkg: file_size=\d* bytes, is_dir=True")

    def test_list_pkg_subdirectory(self):
        """Test listing the contents of a subdirectory."""
        result = get_files_info(WORKING_DIR, "pkg")

        self.assertRegex(result, r"- __init__\.py: file_size=\d* bytes, is_dir=False")
        self.assertRegex(result, r"- calculator\.py: file_size=\d* bytes, is_dir=False")
        self.assertRegex(result, r"- render\.py: file_size=\d* bytes, is_dir=False")

    def test_prohibited_absolute_path(self):
        """Test that inspecting an absolute path outside the project raises an error."""
        with self.assertRaises(ValueError):
            _ = get_files_info(WORKING_DIR, "/etc")

    def test_prohibited_parent_directory(self):
        """Test that directory traversal ('../') is not allowed."""
        with self.assertRaises(ValueError):
            _ = get_files_info(WORKING_DIR, "../")

    def test_non_existent_directory(self):
        """Test that inspecting a non-existent directory raises an error."""
        with self.assertRaises(FileNotFoundError):
            _ = get_files_info(WORKING_DIR, "this_dir_does_not_exist")


if __name__ == "__main__":
    _ = unittest.main()
