import logging
import os
import subprocess
import unittest
from pathlib import Path
from typing import final, override

from .utils import WORKING_DIR

# This script assumes it's run from the project root directory
# where 'main.py' is located.

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent
MAIN_SCRIPT_PATH = PROJECT_ROOT / "main.py"


@final
class TestAgentFunctionCalls(unittest.TestCase):
    """Tests the output of call function on available tools."""

    def __init__(self, method_name: str = "runTest") -> None:
        """Initiate the test class."""
        super().__init__(method_name)
        self.original_cwd: Path = Path.cwd()

    @override
    @classmethod
    def setUpClass(cls) -> None:
        """Set up a dedicated workspace for tests to run in."""
        # Create dummy files for testing
        _ = (WORKING_DIR / "lorem.txt").write_text("wait, this isn't lorem ipsum")
        _ = (WORKING_DIR / "tests.py").write_text('print("Ran 9 tests")')

    def _run_agent(self, prompt: str) -> subprocess.CompletedProcess[str]:
        """Helper function to run the agent with a given prompt."""
        command = ["uv", "run", str(MAIN_SCRIPT_PATH), prompt, "--verbose"]
        return subprocess.run(command, capture_output=True, text=True, check=False)

    def test_run_python_script_success(self) -> None:
        """Test running a simple python script that should succeed."""
        result = self._run_agent("run tests.py")
        self.assertIn("Ran 9 tests", result.stdout)

    def test_read_file_contents(self) -> None:
        """Test reading the contents of an existing file."""
        result = self._run_agent("get the contents of lorem.txt")
        self.assertIn("wait, this isn't lorem ipsum", result.stdout)

    def test_read_nonexistent_file(self) -> None:
        """Test attempting to read a file that does not exist."""
        result = self._run_agent("get the contents of non_existent_file.txt")
        self.assertTrue("Error: " in result.stdout)
        self.assertIn("No such file or directory", result.stdout)

    def test_create_new_file(self) -> None:
        """Test creating a new file with specified content."""
        if (WORKING_DIR / "README.md").exists():
            Path.unlink(WORKING_DIR / "README.md")
        logger.info(WORKING_DIR / "README.md")
        result = self._run_agent("create a new README.md file with the contents '# calculator'")
        self.assertTrue((WORKING_DIR / "README.md").exists())
        self.assertEqual((WORKING_DIR / "README.md").read_text(), "# calculator")

    def test_list_files_in_root(self) -> None:
        """Test listing files in the current directory."""
        # First, create a file to ensure the listing is accurate for the test state
        _ = (WORKING_DIR / "README.md").write_text("temp")

        result = self._run_agent("what files are in the root?")
        # Order might vary, so check for presence of each expected file
        self.assertIn("lorem.txt", result.stdout)
        self.assertIn("README.md", result.stdout)
        self.assertIn("tests.py", result.stdout)


if __name__ == "__main__":
    _ = unittest.main()
