# tests.py

import os
import unittest
from pathlib import Path
from typing import final, override

from ai_agent.functions.get_files_info import get_files_info


@final
class TestFiles(unittest.TestCase):
    @override
    def setUp(self) -> None:
        """Set up the test environment.

        If the tests are being run from the project's 'tests' directory,
        this changes the current working directory to the package's source
        directory to ensure file paths are resolved correctly during the test.
        """
        self.original_cwd = Path.cwd()  # pyright: ignore[reportUninitializedInstanceVariable]
        # Check if the current directory is named 'tests'
        if self.original_cwd.name == "tests":
            # Construct the path to the target directory
            # This goes up one level from 'tests' to the project root,
            # then into 'src/ai_agent'
            project_root = self.original_cwd.parent
            target_dir = project_root / "src" / "ai_agent"

            # Change directory if the target exists
            if target_dir.is_dir():
                os.chdir(target_dir)

    @override
    def tearDown(self) -> None:
        """Tear down the test environment.

        Restores the original working directory after the test has run
        to prevent side effects on other tests.
        """
        os.chdir(self.original_cwd)

    def test_root(self):
        result = get_files_info("calculator", ".")
        expected = (
            "- pkg: file_size=4096 bytes, is_dir=True\n"
            "- calc.py: file_size=1193 bytes, is_dir=False\n"
            "- main.py: file_size=1193 bytes, is_dir=False\n"
            "- __pycache__: file_size=4096 bytes, is_dir=True\n"
            "- __init__.py: file_size=0 bytes, is_dir=False\n"
        )
        self.assertEqual(result, expected)

    def test_pkg(self):
        result = get_files_info("calculator", "pkg")
        # TODO: expected is wrong
        expected = (
            "- __init__.py: file_size=0 bytes, is_dir=False\n"
            "- __pycache__: file_size=4096 bytes, is_dir=True\n"
        )
        self.assertEqual(result, expected)

    def test_bin(self):
        result = get_files_info("calculator", "/bin")
        expected = "Error: Cannot list '/bin' as it is outside the permitted working directory"
        self.assertEqual(result, expected)

    def test_parent(self):
        result = get_files_info("calculator", "../")
        expected = "Error: Cannot list '../' as it is outside the permitted working directory"
        self.assertEqual(result, expected)


if __name__ == "__main__":
    _ = unittest.main()
