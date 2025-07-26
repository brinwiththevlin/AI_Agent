import unittest

from ai_agent.functions.get_files_info import get_files_info

from .utils import WORKING_DIR


class TestFileInfo(unittest.TestCase):
    """Test suite for the get_files_info function."""

    def test_list_calculator_directory(self) -> None:
        """Test listing the contents of the 'calculator' directory."""
        result = get_files_info(WORKING_DIR, ".")
        print(result)

        self.assertRegex(result, r"- __init__\.py: file_size=\d* bytes, is_dir=False")
        self.assertRegex(result, r"- main\.py: file_size=\d* bytes, is_dir=False")
        self.assertRegex(result, r"- calc\.py: file_size=\d* bytes, is_dir=False")
        self.assertRegex(result, r"- pkg: file_size=\d* bytes, is_dir=True")

    def test_list_pkg_subdirectory(self) -> None:
        """Test listing the contents of a subdirectory."""
        result = get_files_info(WORKING_DIR, "pkg")
        print(result)

        self.assertRegex(result, r"- __init__\.py: file_size=\d* bytes, is_dir=False")
        self.assertRegex(result, r"- calculator\.py: file_size=\d* bytes, is_dir=False")
        self.assertRegex(result, r"- render\.py: file_size=\d* bytes, is_dir=False")

    def test_prohibited_absolute_path(self) -> None:
        """Test that inspecting an absolute path outside the project raises an error."""
        result = get_files_info(WORKING_DIR, "/etc")
        print(result)
        self.assertIn("Error:", result)

    def test_prohibited_parent_directory(self) -> None:
        """Test that directory traversal ('../') is not allowed."""
        result = get_files_info(WORKING_DIR, "../")
        print(result)
        self.assertIn("Error:", result)

    def test_non_existent_directory(self) -> None:
        """Test that inspecting a non-existent directory raises an error."""
        result = get_files_info(WORKING_DIR, "this_dir_does_not_exist")
        print(result)
        self.assertIn("Error:", result)


if __name__ == "__main__":
    _ = unittest.main()
