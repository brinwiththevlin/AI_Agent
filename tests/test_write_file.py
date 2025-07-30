import unittest
from pathlib import Path

from ai_agent.functions.write_file import write_file

from .utils import WORKING_DIR


class TestWriteFile(unittest.TestCase):
    """Test suite for write_file."""

    def test_lorem(self) -> None:
        """Test that lorem.txt gets created."""
        result = write_file(WORKING_DIR, "lorem.txt", "wait, this isn't lorem ipsum")
        print(result)
        self.assertRegex(
            result, r"Successfully wrote to '.*' \(\d* characters written\)"
        )

    def test_more_lorem(self) -> None:
        """Test that morelorem.txt gets created."""
        result = write_file(
            WORKING_DIR, "pkg/morelorem.txt", "lorem ipsum dolor sit amet"
        )
        print(result)
        self.assertRegex(
            result, r"Successfully wrote to '.*' \(\d* characters written\)"
        )

    def test_prohibited_write(self) -> None:
        """Test that prohibited paths 'throw' an error."""
        result = write_file(
            WORKING_DIR, "/tmp/temp.txt", "this should not be allowed"
        )  # noqa: S108
        print(result)
        self.assertTrue(result.startswith("Error:"))


if __name__ == "__main__":
    _ = unittest.main()
