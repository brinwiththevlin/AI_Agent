from pathlib import Path
from ai_agent.constants import WORKING_DIRECTORY

FILE_PATH = Path(__file__)
PROJECT_ROOT = (
    Path(__file__).parent.parent
    if FILE_PATH.parent.name == "tests"
    else Path(__file__).parent.parent.parent
)

WORKING_DIR: Path = (PROJECT_ROOT / WORKING_DIRECTORY).resolve()
