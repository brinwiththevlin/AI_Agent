from pathlib import Path

FILE_PATH = Path(__file__)
PROJECT_ROOT = (
    Path(__file__).parent.parent
    if FILE_PATH.parent.name == "tests"
    else Path(__file__).parent.parent.parent
)

WORKING_DIR: str = str((PROJECT_ROOT / "src" / "ai_agent" / "calculator").resolve())
